locals {
  flagsmith_base_url = "https://api.flagsmith.com/api/v1/projects/${var.project_uuid}"
  existing_feature = jsondecode(data.http.read_created_feature.response_body)
  feature_exists = lookup(local.existing_feature, "id", "") != ""
}

data "http" "create_feature" {
  count = local.feature_exists ? 0 : 1

  url = "${local.flagsmith_base_url}/features/"
  method = "POST"

  request_headers = {
    Authorization = "Token ${var.flagsmith_api_key}"
    Content-Type = "application/json"
  }

  request_body = jsonencode({
    name = var.feature_name
    description = var.feature_description
    type = var.feature_type
  })
}

data "http" "set_feature_state" {
  count = local.feature_exists ? 1 : 0

  url = "${local.flagsmith_base_url}/features/${jsondecode(data.http.create_feature[0].response_body).id}/feature-states/"
  method = "POST"

  request_headers = {
    Authorization = "Token ${var.flagsmith_api_key}"
    Content-Type = "application/json"
  }

  request_body = jsonencode({
    feature_state_value = var.feature_state_value
    enabled = var.feature_enabled
  })

  depends_on = [data.http.create_feature]
}


data "http" "read_created_feature" {
  url = "${local.flagsmith_base_url}/features/?name=${urlencode(var.feature_name)}"
  method = "GET"

  request_headers = {
    Authorization = "Token ${var.flagsmith_api_key}"
    Content-Type = "application/json"
  }
}

data "http" "modify_feature_if_changed" {
  count = local.feature_exists ? 1 : 0

  url = "${local.flagsmith_base_url}/features/${local.existing_feature["id"]}"
  method = "POST"

  request_headers = {
    Authorization = "Token ${var.flagsmith_api_key}"
    Content-Type = "application/json"
  }

  request_body = jsonencode({
    description = var.feature_description
    type = var.feature_type
    feature_state_value = var.feature_state_value
    enabled = var.feature_enabled
  })
}
