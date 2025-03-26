<template>
	<Layout>
		<router-view v-if="isReady"></router-view>
	</Layout>
	<Dialogs />
	<Toasts />
</template>

<script setup>
import { Toasts } from 'frappe-ui'
import { Dialogs } from '@/utils/dialogs'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useScreenSize } from './utils/composables'
import DesktopLayout from './components/DesktopLayout.vue'
import MobileLayout from './components/MobileLayout.vue'
import NoSidebarLayout from './components/NoSidebarLayout.vue'
import { stopSession } from '@/telemetry'
import { init as initTelemetry } from '@/telemetry'
import { usersStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const screenSize = useScreenSize()
let { userResource } = usersStore()
const router = useRouter()
const noSidebar = ref(false)
const authStore = useAuthStore()
const isReady = ref(false)

router.beforeEach((to, from, next) => {
	if (to.query.fromLesson) {
		noSidebar.value = true
	} else {
		noSidebar.value = false
	}
	next()
})

const Layout = computed(() => {
	if (noSidebar.value) {
		return NoSidebarLayout
	}
	if (screenSize.width < 640) {
		return MobileLayout
	} else {
		return DesktopLayout
	}
})

onMounted(async () => {
	if (userResource.data) await initTelemetry()
	try {
		await authStore.fetchUserData()
	} catch (error) {
		console.error('Failed to fetch user data:', error)
	} finally {
		isReady.value = true
	}
})

onUnmounted(() => {
	noSidebar.value = false
	stopSession()
})
</script>

<style>
#app {
	font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
	-webkit-font-smoothing: antialiased;
	-moz-osx-font-smoothing: grayscale;
	text-align: center;
	color: #2c3e50;
	margin-top: 60px;
}
</style>
