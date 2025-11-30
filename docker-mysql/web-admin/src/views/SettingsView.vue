<template>
  <div class="max-w-3xl mx-auto p-6">
    <h2 class="text-2xl font-bold mb-6">编辑资料</h2>

    <div v-if="loading" class="text-gray-500">加载中...</div>
    <div v-if="error" class="text-red-600 mb-4">{{ error }}</div>

    <form
      v-if="form"
      @submit.prevent="handleSubmit"
      class="bg-white shadow p-6 rounded-xl space-y-6"
    >
      <!-- Avatar -->
      <div class="flex items-center space-x-6">
        <img
          v-if="preview || form.avatar"
          :src="preview || form.avatar"
          class="w-24 h-24 rounded-full object-cover"
        />

        <div>
          <label class="block font-medium mb-1">上传新头像</label>
          <input
            type="file"
            accept="image/*"
            @change="onAvatarChange"
          />
        </div>
      </div>

      <!-- Username (read-only) -->
      <div>
        <label class="font-medium">用户名</label>
        <input
          type="text"
          v-model="form.username"
          disabled
          class="w-full mt-1 border rounded-md px-3 py-2 bg-gray-100 text-gray-500"
        />
      </div>

      <!-- Nickname -->
      <div>
        <label class="font-medium">昵称</label>
        <input
          type="text"
          v-model="form.nickname"
          class="w-full mt-1 border rounded-md px-3 py-2"
        />
      </div>

      <!-- Email -->
      <div>
        <label class="font-medium">邮箱</label>
        <input
          type="email"
          v-model="form.email"
          class="w-full mt-1 border rounded-md px-3 py-2"
        />
        <p v-if="errors.email" class="text-red-600 text-sm">{{ errors.email }}</p>
      </div>

      <!-- Phone -->
      <div>
        <label class="font-medium">手机号</label>
        <input
          type="text"
          v-model="form.phone_number"
          class="w-full mt-1 border rounded-md px-3 py-2"
        />
        <p v-if="errors.phone_number" class="text-red-600 text-sm">
          {{ errors.phone_number }}
        </p>
      </div>

      <!-- Bio -->
      <div>
        <label class="font-medium">简介</label>
        <textarea
          v-model="form.bio"
          rows="4"
          class="w-full mt-1 border rounded-md px-3 py-2"
        ></textarea>
      </div>

      <div class="flex justify-end">
        <button
          type="submit"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg"
          :disabled="saving"
        >
          {{ saving ? "保存中..." : "保存修改" }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const loading = ref(true);
const saving = ref(false);
const error = ref("");
const errors = ref({}); // 后端字段错误
const form = ref(null);

const preview = ref(null);
let avatarFile = null;

// 加载用户资料 GET
onMounted(async () => {
  try {
    const res = await axios.get("/api/users/me/"); // 你自己的 GET 接口
    form.value = res.data;
  } catch (err) {
    error.value = "无法加载用户资料";
  } finally {
    loading.value = false;
  }
});

// 头像选择
const onAvatarChange = (e) => {
  avatarFile = e.target.files[0];
  if (avatarFile) {
    preview.value = URL.createObjectURL(avatarFile);
  }
};

// 保存 PUT
const handleSubmit = async () => {
  saving.value = true;
  error.value = "";
  errors.value = {};

  try {
    const fd = new FormData();
    fd.append("nickname", form.value.nickname || "");
    fd.append("email", form.value.email || "");
    fd.append("phone_number", form.value.phone_number || "");
    fd.append("bio", form.value.bio || "");

    if (avatarFile) {
      fd.append("avatar", avatarFile);
    }

    const res = await axios.put("/api/users/me/update/", fd, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    // 更新成功，更新页面
    form.value = res.data;
    alert("资料已更新！");

  } catch (err) {
    if (err.response?.data?.errors) {
      errors.value = err.response.data.errors;
    } else {
      error.value = "保存失败，请稍后再试";
    }
  } finally {
    saving.value = false;
  }
};
</script>
