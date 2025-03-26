import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const user = ref(null)
  const isAuthenticated = computed(() => !!user.value)

  const login = async (email, password) => {
    try {
      const response = await fetch('/api/method/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          usr: email,
          pwd: password,
        }),
      })
      
      if (!response.ok) {
        throw new Error('Login failed')
      }

      const data = await response.json()
      user.value = data.user
      router.push('/dashboard')
    } catch (error) {
      console.error('Login error:', error)
      throw error
    }
  }

  const signup = async (formData) => {
    try {
      const response = await fetch('/api/method/lms.lms.user.sign_up', {
        method: 'POST',
        body: formData, // Send as FormData to handle file upload
      })

      if (!response.ok) {
        throw new Error('Signup failed')
      }

      const data = await response.json()
      if (data[0] === 1) {
        // Signup successful, now login
        await login(formData.get('email'), formData.get('password'))
      } else {
        throw new Error(data[1] || 'Signup failed')
      }
    } catch (error) {
      console.error('Signup error:', error)
      throw error
    }
  }

  const googleLogin = async () => {
    try {
      const response = await fetch('/api/method/lms.lms.user.google_login')
      const data = await response.json()
      window.location.href = data.url
    } catch (error) {
      console.error('Google login error:', error)
      throw error
    }
  }

  const switchRole = async (role) => {
    try {
      const response = await fetch('/api/method/lms.lms.user.switch_role', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ role }),
      })

      if (!response.ok) {
        throw new Error('Failed to switch role')
      }

      const data = await response.json()
      if (data.success) {
        // Refresh user data
        await fetchUserData()
      }
    } catch (error) {
      console.error('Role switch error:', error)
      throw error
    }
  }

  const logout = async () => {
    try {
      await fetch('/api/method/logout', { method: 'POST' })
      user.value = null
      router.push('/login')
    } catch (error) {
      console.error('Logout error:', error)
      throw error
    }
  }

  const fetchUserData = async () => {
    try {
      const response = await fetch('/api/method/frappe.client.get_user')
      const data = await response.json()
      user.value = data.message
    } catch (error) {
      console.error('Failed to fetch user data:', error)
      throw error
    }
  }

  // Initialize user data on store creation
  fetchUserData()

  return {
    user,
    isAuthenticated,
    login,
    signup,
    googleLogin,
    switchRole,
    logout,
    fetchUserData,
  }
}) 