<template>
  <div class="workflow-container h-screen flex flex-col">
    <!-- 工作流画布 -->
    <div class="flex-1 relative flex">
      <VueFlow
        :nodes="nodes"
        :edges="edges"
        fit-view
        @node-click="onNodeClick"
        @pane-click="onPaneClick"
        @nodes-change="onNodesChange"
        @edges-change="onEdgesChange"
        class="bg-gray-50 flex-1"
        :node-types="nodeTypes"
      >
        <vue-flow-controls />
        <vue-flow-background variant="dots" gap="20" size="1" />
      </VueFlow>

      <!-- 属性面板 -->
      <aside
        class="w-80 bg-white border-l shadow-lg p-6 flex-shrink-0 transition-all duration-300"
        :class="{ 'translate-x-0': selectedNode, '-translate-x-80': !selectedNode }"
      >
        <h2 class="text-xl font-bold mb-4 text-gray-800">节点属性</h2>

        <div v-if="selectedNode">
          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-1">节点标签</label>
            <input
              v-model="selectedNode.data.label"
              class="w-full border rounded px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-1">输入数据</label>
            <p class="text-gray-700 font-mono">{{ selectedNode.data.inputData || '空' }}</p>
          </div>

          <div class="mb-4">
            <label class="block text-sm text-gray-500 mb-1">输出数据</label>
            <p class="text-gray-700 font-mono">{{ selectedNode.data.outputData || '空' }}</p>
          </div>

          <button
            @click="deleteNode(selectedNode.id)"
            class="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-md transition"
          >
            删除节点
          </button>
        </div>

        <div v-else class="text-gray-400 text-center mt-20">
          点击节点查看属性
        </div>
      </aside>
    </div>

    <!-- 底部菜单栏 -->
    <div class="bottom-bar bg-gray-100 flex items-center justify-center gap-4 p-2 shadow-lg">
      <button
        @click="addNode('task')"
        class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
      >
        添加任务节点
      </button>
      <button
        @click="addNode('decision')"
        class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition"
      >
        添加决策节点
      </button>
      <button
        @click="runWorkflow"
        class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
      >
        运行工作流
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { VueFlow } from '@vue-flow/core'
import '@vue-flow/core/dist/style.css'
import { nanoid } from 'nanoid'
import CustomNode from './CustomNode.vue'  // 自定义节点组件

// 节点和连线
const nodes = ref([
  { id: 'start', type: 'custom', position: { x: 100, y: 100 }, data: { label: '开始', inputData: null, outputData: null } },
])
const edges = ref([])

// 当前选中节点
const selectedNode = ref(null)

// 自定义节点类型
const nodeTypes = { custom: CustomNode }

// 点击节点
const onNodeClick = (payload) => {
  selectedNode.value = payload.node
}

// 点击空白取消选中
const onPaneClick = () => {
  selectedNode.value = null
}

// 节点变化
const onNodesChange = (changes) => {
  changes.forEach(change => {
    const node = nodes.value.find(n => n.id === change.id)
    if (node) Object.assign(node, change)
  })
}

// 边变化
const onEdgesChange = (changes) => {
  changes.forEach(change => {
    const edge = edges.value.find(e => e.id === change.id)
    if (edge) Object.assign(edge, change)
  })
}

// 添加节点
const addNode = (type) => {
  const id = nanoid()
  nodes.value.push({
    id,
    type: 'custom',
    position: { x: 200 + Math.random() * 400, y: 100 + Math.random() * 300 },
    data: { label: type.toUpperCase(), inputData: null, outputData: null }
  })
}

// 删除节点
const deleteNode = (id) => {
  const index = nodes.value.findIndex(n => n.id === id)
  if (index !== -1) nodes.value.splice(index, 1)
  edges.value = edges.value.filter(e => e.source !== id && e.target !== id)
  selectedNode.value = null
}

// 运行工作流
const runWorkflow = () => {
  const visited = new Set()
  const startNodes = nodes.value.filter(n => n.data.label === '开始')

  const executeNode = (node) => {
    if (!node || visited.has(node.id)) return
    visited.add(node.id)

    node.data.outputData = `${node.data.label} 输出 @${new Date().toLocaleTimeString()}`

    const downstreamEdges = edges.value.filter(e => e.source === node.id)
    downstreamEdges.forEach(e => {
      const targetNode = nodes.value.find(n => n.id === e.target)
      if (targetNode) {
        targetNode.data.inputData = node.data.outputData
        executeNode(targetNode)
      }
    })
  }

  startNodes.forEach(n => executeNode(n))
}
</script>

<style scoped>
.workflow-container {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.bottom-bar {
  flex-shrink: 0;
}

.vue-flow {
  background-color: #f9fafb;
}
</style>
