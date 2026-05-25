from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

# 创建 FastAPI 应用实例
app = FastAPI()

# ========== 1. 基础路由 ==========

@app.get("/")
def root():
    """根路径"""
    return {"message": "Hello FastAPI!", "status": "running"}

@app.get("/ping")
def ping():
    """健康检查"""
    return {"ping": "pong"}

# ========== 2. 路径参数路由 ==========

@app.get("/users/{user_id}")
def get_user(user_id: int):
    """通过路径参数获取用户"""
    return {"user_id": user_id, "name": f"User_{user_id}"}

@app.get("/items/{item_id}")
def get_item(item_id: str, q: Optional[str] = None):
    """路径参数 + 查询参数"""
    return {"item_id": item_id, "query": q}

# ========== 3. 查询参数路由 ==========

@app.get("/search")
def search(q: str, page: int = 1, size: int = 10):
    """使用查询参数搜索，带默认值"""
    return {
        "query": q,
        "page": page,
        "size": size,
        "results": [f"Result_{i}" for i in range(min(size, 5))]
    }

# ========== 4. POST 请求路由（带请求体） ==========

class Item(BaseModel):
    name: str
    price: float
    is_available: bool = True
    tags: Optional[list[str]] = []

@app.post("/items")
def create_item(item: Item):
    """创建新商品"""
    return {
        "message": "Item created successfully",
        "item": item
    }

@app.post("/users/{user_id}/orders")
def create_order(user_id: int, item_ids: list[int]):
    """路径参数 + 请求体"""
    return {
        "user_id": user_id,
        "item_ids": item_ids,
        "total_price": len(item_ids) * 99.99,
        "message": "Order created"
    }

# ========== 5. PUT 更新路由 ==========

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """更新商品信息"""
    return {
        "item_id": item_id,
        "updated_item": item,
        "message": "Item updated"
    }

# ========== 6. DELETE 路由 ==========

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    """删除商品"""
    return {"message": f"Item {item_id} has been deleted"}

# ========== 7. 状态码控制 ==========

@app.post("/register", status_code=201)
def register(username: str, password: str):
    """注册用户，返回201创建成功状态码"""
    return {"username": username, "message": "User created"}

# ========== 8. 可选参数和验证 ==========

@app.get("/products/{product_id}")
def get_product(
    product_id: int = Path(..., title="商品ID", ge=1, le=1000),  # 路径参数，范围1-1000
    category: str = Query("all", title="分类", min_length=1, max_length=50)  # 查询参数，有限制
):
    """带验证的路由示例"""
    return {
        "product_id": product_id,
        "category": category,
        "message": f"Product {product_id} in category {category}"
    }