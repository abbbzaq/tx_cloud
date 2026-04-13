# tx_cloud

统一查询多云（阿里云 / 腾讯云 / UCloud）负载均衡信息的 Django REST 服务。

## 功能概览

- 查询阿里云 SLB / ALB / NLB 信息
- 查询腾讯云 CLB / SLB 信息
- 查询 UCloud ULB / NLB 信息
- 将查询结果写入本地数据库（默认 SQLite）
- 提供统一 API 接口返回结果

## 技术栈

- Python 3
- Django 4.2
- Django REST framework
- SQLite（默认）

## 项目结构

```text
tx_cloud/
├── api/                # 业务代码（视图、模型、序列化等）
├── config/             # Django 配置与云厂商配置
├── manage.py
└── requirements.txt
```

## 环境准备

1. 创建并激活虚拟环境
2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 初始化数据库

```bash
python manage.py migrate
```

4. 启动服务

```bash
python manage.py runserver 0.0.0.0:8000
```

## 配置说明

### 1) 环境变量（阿里云 / 腾讯云）

在运行前设置以下环境变量：

- `ALIYUN_ACCESS_KEY_ID`
- `ALIYUN_ACCESS_KEY_SECRET`
- `ALIYUN_REGION_ID`（默认 `cn-beijing`）
- `TENCENT_SECRET_ID`
- `TENCENT_SECRET_KEY`

### 2) 配置文件（UCloud）

编辑 `config/config.yaml`：

- `ucloud.region`
- `ucloud.project_id`
- `ucloud.public_key`
- `ucloud.private_key`

## API 使用

基础地址：`http://127.0.0.1:8000`

### 阿里云

- `POST /ali/`
- 请求体示例：

```json
{
  "lb_type": "slb"
}
```

`lb_type` 支持：`slb` / `alb` / `nlb`

### 腾讯云

- `POST /tx/`
- 请求体示例：

```json
{
  "lb_type": "clb"
}
```

`lb_type` 支持：`clb` / `slb`

### UCloud

- `POST /ucloud/`
- 请求体示例：

```json
{
  "lb_type": "ulb"
}
```

`lb_type` 支持：`ulb` / `nlb`

## 注意事项

- 当前项目默认 `DEBUG=True`，仅建议在开发环境使用。
- 数据库存储为本地 `db.sqlite3`，请按需切换生产数据库。
- 若云厂商凭证或权限不正确，接口会返回对应错误信息。
