schema "info_retrieval" {
  charset = "utf8mb3"
  collate = "utf8mb3_bin"
}

table tbl_users {
    schema = schema.info_retrieval

    column id {
        type = varchar(32)
    }

    column username {
        type = varchar(32)
    }

    column hashed_password {
        type = varchar(64)
    }

    primary_key {
        columns = [column.id]
    }

    index idx_username{
        unique = true
        columns = [column.username]
    }
}

table tbl_bookmarks {
    schema = schema.info_retrieval

    column id {
        type = varchar(32)
    }

    column user_id {
        type = varchar(32)
    }

    column recipe_id {
        type = int
    }

    column rating {
        type = int
    }

    check "rating >= 1 and rating <= 5" {
        expr = "rating >= 1 and rating <= 5"
    }

    index idx_user_recipe{
        unique = true
        columns = [column.user_id, column.recipe_id]
    }
}