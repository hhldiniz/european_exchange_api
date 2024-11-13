resource "aws_dynamodb_table" "dynamodb_table" {
  name           = var.table_name
  hash_key       = var.hash_key
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity

  # Hash Key
  attribute {
    name = var.hash_key
    type = var.hash_key_type
  }

  # Additional attributes
  dynamic "attribute" {
    for_each = var.attributes
    content {
      name = attribute.value.name
      type = attribute.value.type
    }
  }

  # Global Secondary Indexes

  dynamic "global_secondary_index" {
    for_each = var.global_secondary_indexes
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.hash_key
      projection_type = global_secondary_index.value.projection_type
    }
  }

  #Local Secondary Indexes

  dynamic "local_secondary_index" {
    for_each = var.local_secondary_indexes
    content {
      name            = local_secondary_index.value.name
      projection_type = local_secondary_index.value.projection_type
      range_key       = local_secondary_index.value.range_key
    }
  }

  tags = var.tags
}