output "feature_id" {
  value = try(
    jsondecode(data.http.create_feature[0].response_body).id,
    jsondecode(data.http.read_created_feature.response_body).id,
    null
  )
}