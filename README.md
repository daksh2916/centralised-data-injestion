# 📦 API Logger for FastAPI

`api-logger` is a **FastAPI middleware** that automatically logs **all incoming requests and outgoing responses** and uploads them (including files) to your **S3 bucket**.  

This package helps you track and debug your APIs by persisting request/response payloads in a structured way.

---

## ✨ Features

- ✅ Logs every API **request** and **response**
- ✅ Handles JSON bodies, form data, and file uploads
- ✅ Stores logs in **Amazon S3**
- ✅ Easy integration with any FastAPI project
- ✅ Customizable S3 path prefix for organized logging

---

## 🚀 Installation

```bash
pip install api-logger
