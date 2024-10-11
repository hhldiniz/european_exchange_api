resource "render_web_service" "web" {
  name               = var.app_name
  plan               = "starter"
  region             = "oregon"
  start_command      = "python main.py"
  pre_deploy_command = "echo 'Starting deploy...'"

  runtime_source = {
    native_runtime = {
      auto_deploy   = true
      branch        = "master"
      build_command = "pip install -r requirements.txt"
      build_filter = {
        paths         = ["src/**"]
        ignored_paths = ["tests/**"]
      }
      repo_url = "https://github.com/hhldiniz/european_exchange_api.git"
      runtime  = "python"
    }
  }

  disk = {
    name       = "storage-disk"
    size_gb    = 1
    mount_path = "/data"
  }

  env_vars = {
    "key1" = { value = "val1" },
    "key2" = { value = "val2" },
  }
  secret_files = {
    "file1" = { content = "content1" },
    "file2" = { content = "content2" },
  }
  custom_domains = [
    { name : "terraform-provider-1.example.com" },
    { name : "terraform-provider-2.example.com" },
  ]

  notification_override = {
    preview_notifications_enabled = "false"
    notifications_to_send         = "failure"
  }

  log_stream_override = {
    setting = "drop"
  }
}
