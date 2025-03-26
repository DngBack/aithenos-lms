<template>
	<div
		class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8"
	>
		<div class="max-w-md w-full space-y-8">
			<div>
				<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
					{{ isSignup ? 'Create your account' : 'Sign in to your account' }}
				</h2>
			</div>

			<!-- Avatar Upload Section -->
			<div v-if="isSignup" class="flex justify-center">
				<div class="relative">
					<img
						v-if="avatarPreview"
						:src="avatarPreview"
						class="w-24 h-24 rounded-full object-cover"
						alt="Avatar preview"
					/>
					<div
						v-else
						class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center"
					>
						<UserIcon class="w-12 h-12 text-gray-400" />
					</div>
					<label
						class="absolute bottom-0 right-0 bg-white rounded-full p-1 shadow-lg cursor-pointer"
					>
						<input
							type="file"
							accept="image/*"
							class="hidden"
							@change="handleAvatarChange"
						/>
						<CameraIcon class="w-4 h-4 text-gray-600" />
					</label>
				</div>
			</div>

			<form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
				<!-- Login Form Fields -->
				<div v-if="!isSignup" class="rounded-md shadow-sm -space-y-px">
					<div>
						<label for="email" class="sr-only">Email address</label>
						<input
							id="email"
							v-model="email"
							name="email"
							type="email"
							required
							class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
							placeholder="Email address"
						/>
					</div>
					<div>
						<label for="password" class="sr-only">Password</label>
						<input
							id="password"
							v-model="password"
							name="password"
							type="password"
							required
							class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
							placeholder="Password"
						/>
					</div>
				</div>

				<!-- Signup Form Fields -->
				<template v-if="isSignup">
					<!-- Role Selection -->
					<div class="space-y-4">
						<label class="block text-sm font-medium text-gray-700">Select Role</label>
						<div class="grid grid-cols-2 gap-4">
							<button
								type="button"
								@click="selectedRole = 'Student'"
								class="p-4 border rounded-lg text-center"
								:class="{
									'border-indigo-500 bg-indigo-50': selectedRole === 'Student',
									'border-gray-300': selectedRole !== 'Student'
								}"
							>
								<UserIcon class="w-8 h-8 mx-auto mb-2" />
								<span class="block font-medium">Student</span>
							</button>
							<button
								type="button"
								@click="selectedRole = 'Teacher'"
								class="p-4 border rounded-lg text-center"
								:class="{
									'border-indigo-500 bg-indigo-50': selectedRole === 'Teacher',
									'border-gray-300': selectedRole !== 'Teacher'
								}"
							>
								<AcademicCapIcon class="w-8 h-8 mx-auto mb-2" />
								<span class="block font-medium">Teacher</span>
							</button>
						</div>
					</div>

					<!-- Full Name Field -->
					<div class="rounded-md shadow-sm -space-y-px">
						<div>
							<label for="full_name" class="sr-only">Full Name</label>
							<input
								id="full_name"
								v-model="fullName"
								name="full_name"
								type="text"
								required
								class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Full Name"
							/>
						</div>
					</div>

					<!-- Email and Password Fields -->
					<div class="rounded-md shadow-sm -space-y-px">
						<div>
							<label for="email" class="sr-only">Email address</label>
							<input
								id="email"
								v-model="email"
								name="email"
								type="email"
								required
								class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Email address"
							/>
						</div>
						<div>
							<label for="password" class="sr-only">Password</label>
							<input
								id="password"
								v-model="password"
								name="password"
								type="password"
								required
								class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
								placeholder="Password"
							/>
						</div>
					</div>
				</template>

				<!-- Submit Button -->
				<div>
					<button
						type="submit"
						class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
						:disabled="isLoading"
					>
						<span class="absolute left-0 inset-y-0 flex items-center pl-3">
							<LockClosedIcon v-if="!isSignup" class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" />
							<UserAddIcon v-else class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400" />
						</span>
						{{ isLoading ? (isSignup ? 'Creating account...' : 'Signing in...') : (isSignup ? 'Create account' : 'Sign in') }}
					</button>
				</div>

				<!-- Toggle Signup/Login -->
				<div v-if="!isSignup" class="text-center">
					<button
						type="button"
						@click="toggleMode"
						class="text-sm font-medium text-indigo-600 hover:text-indigo-500"
					>
						Don't have an account? Sign up
					</button>
				</div>

				<!-- Social Login Divider -->
				<div class="relative">
					<div class="absolute inset-0 flex items-center">
						<div class="w-full border-t border-gray-300"></div>
					</div>
					<div class="relative flex justify-center text-sm">
						<span class="px-2 bg-gray-50 text-gray-500">Or continue with</span>
					</div>
				</div>

				<!-- Google Login Button -->
				<div>
					<button
						type="button"
						@click="handleGoogleLogin"
						class="w-full flex items-center justify-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
						:disabled="isLoading"
					>
						<img
							class="h-5 w-5 mr-2"
							src="https://www.google.com/favicon.ico"
							alt="Google logo"
						/>
						{{ isSignup ? 'Sign up with Google' : 'Sign in with Google' }}
					</button>
				</div>

				<!-- Toggle Login/Signup -->
				<div v-if="isSignup" class="text-center">
					<button
						type="button"
						@click="toggleMode"
						class="text-sm font-medium text-indigo-600 hover:text-indigo-500"
					>
						Already have an account? Sign in
					</button>
				</div>
			</form>
		</div>
	</div>
</template>

<script>
import { ref } from 'vue'
import { LockClosedIcon, UserAddIcon, UserIcon, CameraIcon, AcademicCapIcon } from '@heroicons/vue/solid'
import { useAuthStore } from '../stores/auth'

export default {
	name: 'Login',
	components: {
		LockClosedIcon,
		UserAddIcon,
		UserIcon,
		CameraIcon,
		AcademicCapIcon,
	},
	setup() {
		const authStore = useAuthStore()
		const isSignup = ref(false)
		const email = ref('')
		const password = ref('')
		const fullName = ref('')
		const selectedRole = ref('Student')
		const avatarFile = ref(null)
		const avatarPreview = ref(null)
		const isLoading = ref(false)

		const toggleMode = () => {
			isSignup.value = !isSignup.value
			// Reset form when switching modes
			email.value = ''
			password.value = ''
			fullName.value = ''
			avatarFile.value = null
			avatarPreview.value = null
		}

		const handleAvatarChange = (event) => {
			const file = event.target.files[0]
			if (file) {
				avatarFile.value = file
				const reader = new FileReader()
				reader.onload = (e) => {
					avatarPreview.value = e.target.result
				}
				reader.readAsDataURL(file)
			}
		}

		const handleSubmit = async () => {
			try {
				isLoading.value = true
				if (isSignup.value) {
					const formData = new FormData()
					formData.append('full_name', fullName.value)
					formData.append('email', email.value)
					formData.append('password', password.value)
					formData.append('role', selectedRole.value)
					if (avatarFile.value) {
						formData.append('avatar', avatarFile.value)
					}
					await authStore.signup(formData)
				} else {
					await authStore.login(email.value, password.value)
				}
			} catch (error) {
				console.error('Authentication error:', error)
			} finally {
				isLoading.value = false
			}
		}

		const handleGoogleLogin = async () => {
			try {
				isLoading.value = true
				await authStore.googleLogin()
			} catch (error) {
				console.error('Google login failed:', error)
			} finally {
				isLoading.value = false
			}
		}

		return {
			isSignup,
			email,
			password,
			fullName,
			selectedRole,
			avatarPreview,
			isLoading,
			toggleMode,
			handleAvatarChange,
			handleSubmit,
			handleGoogleLogin,
		}
	},
}
</script>
