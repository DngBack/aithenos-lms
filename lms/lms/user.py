import frappe
from frappe import _
from frappe.model.naming import append_number_if_name_exists
from frappe.website.utils import cleanup_page_name
from frappe.website.utils import is_signup_disabled
from frappe.utils import random_string, escape_html
from lms.lms.utils import get_country_code
from frappe.integrations.oauth2 import OAuth2Client
from frappe.integrations.google_oauth import GoogleOAuth2Client


def validate_username_duplicates(doc, method):
	while not doc.username or doc.username_exists():
		doc.username = append_number_if_name_exists(
			doc.doctype, cleanup_page_name(doc.full_name), fieldname="username"
		)
	if " " in doc.username:
		doc.username = doc.username.replace(" ", "")

	if len(doc.username) < 4:
		doc.username = doc.email.replace("@", "").replace(".", "")


def after_insert(doc, method):
	# Add default roles based on user type
	if doc.user_type == "Website User":
		doc.add_roles("LMS Student")
	elif doc.user_type == "Guardian":
		doc.add_roles("LMS Guardian")
	elif doc.user_type == "Teacher":
		doc.add_roles("LMS Teacher")


@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, verify_terms, user_category, auth_provider=None):
	if is_signup_disabled():
		frappe.throw(_("Sign Up is disabled"), _("Not Allowed"))

	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return 0, _("Already Registered")
		else:
			return 0, _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_("Too many users signed up recently, so the registration is disabled. Please try back in an hour"),
				http_status_code=429,
			)

	user = frappe.get_doc(
		{
			"doctype": "User",
			"email": email,
			"first_name": escape_html(full_name),
			"verify_terms": verify_terms,
			"user_category": user_category,
			"country": "",
			"enabled": 1,
			"new_password": random_string(10),
			"user_type": "Website User",
			"auth_provider": auth_provider,  # Store the authentication provider
		}
	)
	user.flags.ignore_permissions = True
	user.flags.ignore_password_policy = True
	user.insert()

	# Set default signup role as per Portal Settings
	default_role = frappe.db.get_single_value("Portal Settings", "default_role")
	if default_role:
		user.add_roles(default_role)

	user.add_roles("LMS Student")
	set_country_from_ip(None, user.name)

	if user.flags.email_sent:
		return 1, _("Please check your email for verification")
	else:
		return 2, _("Please ask your administrator to verify your sign-up")


@frappe.whitelist(allow_guest=True)
def google_login():
	"""Handle Google OAuth2 login"""
	client = GoogleOAuth2Client()
	return client.get_authorization_url()


@frappe.whitelist(allow_guest=True)
def google_callback(code):
	"""Handle Google OAuth2 callback"""
	client = GoogleOAuth2Client()
	user_info = client.get_user_info(code)
	
	if not user_info:
		frappe.throw(_("Failed to get user info from Google"))
	
	email = user_info.get("email")
	full_name = user_info.get("name")
	
	# Check if user exists
	user = frappe.db.get("User", {"email": email})
	if not user:
		# Create new user
		sign_up(email, full_name, 1, "Student", "Google")
		user = frappe.get_doc("User", email)
	
	# Log in the user
	frappe.local.login_manager.login_as(user.name)
	return frappe.local.response


@frappe.whitelist()
def switch_role(role):
	"""Switch user role between Student and Teacher"""
	user = frappe.get_doc("User", frappe.session.user)
	current_roles = user.get_roles()
	
	if role not in ["LMS Student", "LMS Teacher"]:
		frappe.throw(_("Invalid role"))
	
	if role not in current_roles:
		# Add the new role
		user.add_roles(role)
		frappe.db.commit()
	
	# Update session
	frappe.local.session.user_roles = user.get_roles()
	frappe.local.session.update()
	
	return {"success": True, "message": _("Role switched successfully")}


def set_country_from_ip(login_manager=None, user=None):
	if not user and login_manager:
		user = login_manager.user
	user_country = frappe.db.get_value("User", user, "country")
	# if user_country:
	#    return
	frappe.db.set_value("User", user, "country", get_country_code())
	return


def on_login(login_manager):
	default_app = frappe.db.get_single_value("System Settings", "default_app")
	if default_app == "lms":
		frappe.local.response["home_page"] = "/lms"
