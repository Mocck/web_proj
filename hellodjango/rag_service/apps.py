from django.apps import AppConfig

class RagServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rag_service'

    def ready(self):
        # Django 启动时自动执行
        from .rag_loader import load_vectorstore
        try:
            load_vectorstore()
        except Exception as e:
            print(f"⚠️ RAG 初始化失败: {e}")
