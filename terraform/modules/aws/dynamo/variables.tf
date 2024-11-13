variable "table_name" {
  type = string
  description = "DynamoDB table name"
}

variable "read_capacity" {
  type = number
  default = 25
}

variable "write_capacity" {
  type = number
  default = 25
}

variable "hash_key" {
  type = string
  description = "DynamoDB table Hash Key"
}

variable "hash_key_type" {
  type = string
  default = "S"
  description = "Hash Key type, which must be a scalar type: `S`, `N`, or `B` for (S)tring, (N)umber, or (B)inary data"
}

variable "attributes" {
  type        = list(map(string))
  default     = []
  description = "Additional DynamoDB attributes as a list of mapped values"
}

variable "global_secondary_indexes" {
  type        = list(map(string))
  default     = []
  description = "Additional global secondary indexes in the form of a list of mapped values"
}

variable "local_secondary_indexes" {
  type        = list(map(string))
  default     = []
  description = "Additional local secondary indexes in the form of a list of mapped values"
}

variable "tags" {
  type        = map(string)
  default     = {}
  description = "Additional tags (e.g. `map('BusinessUnit','XYZ')`"
}