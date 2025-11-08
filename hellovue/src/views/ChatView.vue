<template>
  <div class="flex h-[calc(100vh-3.5rem)] bg-gray-100">
    <!-- 左侧会话列表 -->
    <aside class="w-64 bg-white border-r shadow-sm p-4 flex flex-col">
      <!-- ✅ 新增：首页按钮 -->
      <button
        @click="goHome"
        class="mb-4 w-full bg-gray-100 hover:bg-blue-100 text-gray-700 font-medium py-2 rounded-lg transition flex items-center justify-center gap-2"
      >
        🏠 返回首页
      </button>

      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-700">会话列表</h2>
        <button
          @click="openCreateDialog = true"
          class="text-sm bg-blue-500 hover:bg-blue-600 text-white px-2 py-1 rounded-md"
        >
          + 新建
        </button>
      </div>

      <div class="flex-1 overflow-y-auto space-y-3">
        <div
          v-for="session in sessions"
          :key="session.id"
          @click="selectSession(session)"
          class="p-3 rounded-lg cursor-pointer flex justify-between items-center hover:bg-blue-100 transition"
          :class="{'bg-blue-200 font-semibold text-blue-700': currentSession?.id === session.id}"
        >
          <span class="truncate">{{ session.title || '未命名会话' }}</span>

          <!-- 三点菜单 -->
          <div class="relative">
            <button
              @click.stop="toggleMenu(session.id)"
              class="text-gray-500 hover:text-gray-700 px-1"
            >⋮</button>

            <div
              v-if="menuOpen === session.id"
              class="absolute right-0 mt-2 w-28 bg-white border rounded-lg shadow-lg z-10"
            >
              <button
                @click.stop="renameSession(session)"
                class="block w-full text-left px-3 py-2 text-sm hover:bg-gray-100"
              >重命名</button>

              <button
                @click.stop="confirmDelete(session)"
                class="block w-full text-left px-3 py-2 text-sm text-red-600 hover:bg-red-50"
              >删除</button>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- 右侧聊天区 -->
    <main class="flex-1 flex flex-col">
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <div v-if="!currentSession" class="text-center text-gray-500 mt-10">
          👈 请选择或新建一个会话
        </div>

        <div v-else>
          <div
            v-for="msg in messages"
            :key="msg.id"
            class="flex"
            :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
          >
            <div
              class="max-w-[70%] px-4 py-2 rounded-xl shadow text-sm whitespace-pre-wrap"
              :class="msg.role === 'user'
                ? 'bg-blue-500 text-white rounded-br-none'
                : 'bg-gray-200 text-gray-800 rounded-bl-none'"
            >
              {{ msg.content }}
            </div>
          </div>
        </div>
      </div>

      <!-- 底部输入框 -->
      <div class="border-t bg-white p-4 flex items-center space-x-2">
        <input
          v-model="input"
          type="text"
          placeholder="输入消息..."
          class="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring focus:ring-blue-300"
          @keyup.enter="sendMessage"
          :disabled="!currentSession || sending"
        />
        <button
          @click="sendMessage"
          :disabled="!currentSession || sending"
          class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        >
          {{ sending ? '生成中...' : '发送' }}
        </button>
      </div>
    </main>

    <!-- ✅ 新建会话对话框 -->
    <div
      v-if="openCreateDialog"
      class="fixed inset-0 bg-black bg-opacity-30 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-80">
        <h3 class="text-lg font-semibold mb-3">新建会话</h3>
        <input
          v-model="newSessionTitle"
          type="text"
          placeholder="请输入会话名称"
          class="w-full border px-3 py-2 rounded-lg mb-4 focus:outline-none focus:ring focus:ring-blue-300"
        />
        <div class="flex justify-end space-x-2">
          <button
            @click="openCreateDialog = false"
            class="px-3 py-1 text-gray-600 hover:text-gray-800"
          >取消</button>
          <button
            @click="createSession"
            class="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded-md"
          >创建</button>
        </div>
      </div>
    </div>

    <!-- ✅ 删除确认框 -->
    <div
      v-if="confirmingDelete"
      class="absolute right-10 top-20 bg-white border rounded-lg shadow-lg p-4 z-50 w-60"
    >
      <p class="text-gray-700 mb-3">确定要删除「{{ deleteTarget?.title || '未命名会话' }}」吗？</p>
      <div class="flex justify-end space-x-2">
        <button @click="cancelDelete" class="px-3 py-1 text-gray-600 hover:text-gray-800">取消</button>
        <button @click="deleteSession(deleteTarget.id)" class="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600">删除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const sessions = ref([])
const currentSession = ref(null)
const messages = ref([])
const input = ref('')
const sending = ref(false)
const menuOpen = ref(null)

const openCreateDialog = ref(false)
const newSessionTitle = ref('')
const confirmingDelete = ref(false)
const deleteTarget = ref(null)

const api = axios.create({
  baseURL: '/api/chat',
  withCredentials: true
})

/* 加载会话列表 */
const loadSessions = async () => {
  try {
    const res = await api.get('/sessions/')
    sessions.value = res.data
  } catch (err) {
    console.error('加载会话失败', err)
  }
}

/* 选择会话 */
const selectSession = async (session) => {
  currentSession.value = session
  await loadMessages(session.id)
}

/* 加载消息 */
const loadMessages = async (sessionId) => {
  try {
    const res = await api.get('/messages/', { params: { session_id: sessionId } })
    messages.value = res.data
  } catch (err) {
    console.error('加载消息失败', err)
  }
}

/* 发送消息（禁止重复发送中） */
const sendMessage = async () => {
  if (!input.value.trim() || !currentSession.value || sending.value) return
  sending.value = true

  try {
    const res = await api.post('/messages/send/', {
      session_id: currentSession.value.id,
      content: input.value
    })
    messages.value.push(res.data.user_message) // 显示用户消息

    // 模拟等待AI生成回复
    await new Promise(r => setTimeout(r, 3000))
    await loadMessages(currentSession.value.id)
  } catch (err) {
    console.error('发送失败', err)
  } finally {
    input.value = ''
    sending.value = false
  }
}

/* 新建会话 */
const createSession = async () => {
  try {
    const res = await api.post('/sessions/create/', { title: newSessionTitle.value })
    sessions.value.unshift(res.data)
    currentSession.value = res.data
    messages.value = []
    newSessionTitle.value = ''
    openCreateDialog.value = false
  } catch (err) {
    console.error('创建会话失败', err)
  }
}

/* 删除逻辑 */
const confirmDelete = (session) => {
  confirmingDelete.value = true
  deleteTarget.value = session
  menuOpen.value = null
}

const cancelDelete = () => {
  confirmingDelete.value = false
  deleteTarget.value = null
}

const deleteSession = async (id) => {
  try {
    await api.delete(`/sessions/${id}/`)
    if (currentSession.value?.id === id) {
      currentSession.value = null
      messages.value = []
    }
    await loadSessions()
  } catch (err) {
    console.error('删除失败', err)
  } finally {
    confirmingDelete.value = false
  }
}

/* ✅ 返回首页 */
const goHome = () => {
  router.push('/home')
}

/* 重命名逻辑 */
const renameSession = async (session) => {
  const newName = prompt('请输入新的会话名称', session.title)
  if (!newName || newName === session.title) return
  try {
    await api.patch(`/sessions/${session.id}/`, { title: newName })
    session.title = newName
  } catch (err) {
    console.error('重命名失败', err)
  }
  menuOpen.value = null
}

/* 打开菜单 */
const toggleMenu = (id) => {
  menuOpen.value = menuOpen.value === id ? null : id
}

/* 初始化加载 */
onMounted(() => {
  loadSessions()
})
</script>
