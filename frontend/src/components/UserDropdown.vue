<template>
	<div class="relative">
		<button
			@click="toggleDropdown"
			class="flex items-center space-x-2 focus:outline-none"
		>
			<UserAvatar :user="user" />
			<span class="text-gray-700">{{ user.full_name }}</span>
			<ChevronDownIcon class="w-4 h-4 text-gray-500" />
		</button>

		<div
			v-if="isOpen"
			class="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-50"
		>
			<!-- Role Switch Section -->
			<div v-if="hasMultipleRoles" class="px-4 py-2 border-b">
				<p class="text-sm text-gray-500 mb-2">Switch Role</p>
				<div class="space-y-2">
					<button
						v-for="role in availableRoles"
						:key="role"
						@click="switchRole(role)"
						class="w-full text-left px-2 py-1 text-sm rounded hover:bg-gray-100"
						:class="{ 'bg-gray-100': currentRole === role }"
					>
						{{ role === 'LMS Student' ? 'Student View' : 'Teacher Studio' }}
					</button>
				</div>
			</div>

			<!-- Navigation Links -->
			<router-link
				to="/profile"
				class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
				@click="isOpen = false"
			>
				Profile
			</router-link>
			<router-link
				to="/settings"
				class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
				@click="isOpen = false"
			>
				Settings
			</router-link>

			<!-- Logout Button -->
			<button
				@click="logout"
				class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
				@click="isOpen = false"
			>
				Logout
			</button>
		</div>
	</div>
</template>

<script setup>
import LMSLogo from '@/components/Icons/LMSLogo.vue'
import { sessionStore } from '@/stores/session'
import { Dropdown } from 'frappe-ui'
import Apps from '@/components/Apps.vue'
import { useRouter } from 'vue-router'
import { convertToTitleCase } from '@/utils'
import { usersStore } from '@/stores/user'
import { useSettings } from '@/stores/settings'
import { markRaw, watch, ref, onMounted, computed } from 'vue'
import { createDialog } from '@/utils/dialogs'
import SettingsModal from '@/components/Modals/Settings.vue'
import FrappeCloudIcon from '@/components/Icons/FrappeCloudIcon.vue'
import {
	ChevronDown,
	LogIn,
	LogOut,
	Moon,
	User,
	Settings,
	Sun,
	Zap,
} from 'lucide-vue-next'
import UserAvatar from './UserAvatar.vue'
import { ChevronDownIcon } from '@heroicons/vue/solid'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const { logout, branding } = sessionStore()
let { userResource } = usersStore()
const settingsStore = useSettings()
let { isLoggedIn } = sessionStore()
const showSettingsModal = ref(false)
const theme = ref('light')
const frappeCloudBaseEndpoint = 'https://frappecloud.com'
const $dialog = createDialog
const authStore = useAuthStore()
const isOpen = ref(false)
const user = computed(() => authStore.user)

const props = defineProps({
	isCollapsed: {
		type: Boolean,
		default: false,
	},
})

onMounted(() => {
	theme.value = localStorage.getItem('theme') || 'light'
	if (['light', 'dark'].includes(theme.value)) {
		document.documentElement.setAttribute('data-theme', theme.value)
	}
})

watch(
	() => settingsStore.isSettingsOpen,
	(value) => {
		showSettingsModal.value = value
	}
)

const toggleTheme = () => {
	const currentTheme = document.documentElement.getAttribute('data-theme')
	theme.value = currentTheme === 'dark' ? 'light' : 'dark'
	document.documentElement.setAttribute('data-theme', theme.value)
	localStorage.setItem('theme', theme.value)
}

const userDropdownOptions = computed(() => {
	return [
		{
			group: '',
			items: [
				{
					icon: User,
					label: 'My Profile',
					onClick: () => {
						router.push(`/user/${userResource.data?.username}`)
					},
					condition: () => {
						return isLoggedIn
					},
				},
				{
					icon: theme.value === 'light' ? Moon : Sun,
					label: 'Toggle Theme',
					onClick: () => {
						toggleTheme()
					},
				},
				{
					component: markRaw(Apps),
					condition: () => {
						let cookies = new URLSearchParams(
							document.cookie.split('; ').join('&')
						)
						let system_user = cookies.get('system_user')
						if (system_user === 'yes') return true
						else return false
					},
				},
				{
					icon: Settings,
					label: 'Settings',
					onClick: () => {
						settingsStore.isSettingsOpen = true
					},
					condition: () => {
						return userResource.data?.is_moderator
					},
				},
				{
					icon: FrappeCloudIcon,
					label: 'Login to Frappe Cloud',
					onClick: () => {
						$dialog({
							title: __('Login to Frappe Cloud?'),
							message: __(
								'Are you sure you want to login to your Frappe Cloud dashboard?'
							),
							actions: [
								{
									label: __('Confirm'),
									variant: 'solid',
									onClick(close) {
										loginToFrappeCloud()
										close()
									},
								},
							],
						})
					},
					condition: () => {
						return (
							userResource.data?.is_system_manager &&
							userResource.data?.is_fc_site
						)
					},
				},
			],
		},
		{
			group: '',
			items: [
				{
					icon: Zap,
					label: 'Powered by Learning',
					onClick: () => {
						window.open('https://frappe.io/learning', '_blank')
					},
				},
				{
					icon: LogOut,
					label: 'Log out',
					onClick: () => {
						logout.submit().then(() => {
							isLoggedIn = false
						})
					},
					condition: () => {
						return isLoggedIn
					},
				},
				{
					icon: LogIn,
					label: 'Log in',
					onClick: () => {
						window.location.href = '/login'
					},
					condition: () => {
						return !isLoggedIn
					},
				},
			],
		},
	]
})

const loginToFrappeCloud = () => {
	let redirect_to = '/dashboard/sites/' + userResource.data.sitename
	window.open(`${frappeCloudBaseEndpoint}${redirect_to}`, '_blank')
}

const currentRole = computed(() => {
	const roles = user.value?.roles || []
	if (roles.includes('LMS Teacher')) return 'LMS Teacher'
	return 'LMS Student'
})

const hasMultipleRoles = computed(() => {
	const roles = user.value?.roles || []
	return roles.includes('LMS Student') && roles.includes('LMS Teacher')
})

const availableRoles = computed(() => {
	const roles = user.value?.roles || []
	return roles.filter((role) => ['LMS Student', 'LMS Teacher'].includes(role))
})

const toggleDropdown = () => {
	isOpen.value = !isOpen.value
}

const switchRole = async (role) => {
	try {
		await authStore.switchRole(role)
		// Redirect based on role
		if (role === 'LMS Teacher') {
			router.push('/studio')
		} else {
			router.push('/dashboard')
		}
	} catch (error) {
		console.error('Failed to switch role:', error)
	}
}

const logout = async () => {
	await authStore.logout()
	router.push('/login')
}
</script>
