# Day 12 Lab - Mission Answers

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. **Hardcoded Secrets**: API Key (`sk-...`) được viết trực tiếp trong code, dễ bị lộ khi commit.
2. **Fixed Configuration**: Port và Host bị cố định, không linh hoạt khi chạy trên các môi trường khác nhau.
3. **Lack of Observability**: Sử dụng `print()` thay vì structured logging, khó quản lý log tập trung.
4. **No Health Checks**: Không có endpoint `/health` khiến hệ thống điều phối (Orchestrator) không biết trạng thái ứng dụng.
5. **Abrupt Shutdown**: Không xử lý tín hiệu SIGTERM, dẫn đến việc ngắt kết nối đột ngột khi stop container.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Tại sao quan trọng? |
|---------|-------|----------|---------------------|
| Config | Hardcode | Env vars | Bảo mật thông tin nhạy cảm và linh hoạt giữa các môi trường (Dev/Staging/Prod). |
| Health check | Không có | Endpoints (/health, /ready) | Giúp Cloud Platform tự động restart khi app treo và điều phối traffic chính xác. |
| Logging | print() | JSON Structured Log | Dễ dàng parse log bởi các công cụ như ELK, CloudWatch để giám sát và debug. |
| Shutdown | Đột ngột | Graceful (SIGTERM) | Đảm bảo các request đang xử lý được hoàn thành, tránh mất dữ liệu hoặc lỗi client. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. **Base image là gì?**: `python:3.11-slim` (image nhẹ, tối ưu cho runtime).
2. **Working directory là gì?**: `/app`.
3. **Tại sao COPY requirements.txt trước?**: Để tận dụng Docker Layer Caching. Dependencies chỉ được cài lại nếu file requirements thay đổi, giúp build nhanh hơn.
4. **CMD vs ENTRYPOINT khác nhau thế nào?**: CMD cung cấp các tham số mặc định có thể ghi đè khi chạy container, trong khi ENTRYPOINT thiết lập lệnh thực thi chính khó bị ghi đè hơn.

### Exercise 2.3: Image size comparison
- **Develop**: ~800 MB (Sử dụng full python image).
- **Production**: ~150 MB (Sử dụng slim image và multi-stage build).
- **Difference**: Giảm khoảng 80% dung lượng.

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- **URL**: https://agent-lab12-nguyentiendung.up.railway.app (Ví dụ)
- **Screenshot**: [N/A - See DEPLOYMENT.md]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- **Auth**: Trả về 401 nếu thiếu API Key.
- **Rate Limit**: Trả về 429 sau 10 requests/phút (đã test với loop).

### Exercise 4.4: Cost guard implementation
Logic: Sử dụng biến toàn cục (trong môi trường lab) hoặc Redis để lưu trữ `current_cost`. Trước mỗi request `/ask`, hệ thống kiểm tra chi phí tích lũy của `user_id`. Nếu vượt mức `DAILY_BUDGET_USD` trong `config.py`, hệ thống sẽ từ chối xử lý và trả về lỗi 402.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- **Liveness/Readiness**: Đã implement endpoint `/health` (check process) và `/ready` (check app initialization).
- **Graceful Shutdown**: Sử dụng `asynccontextmanager` (lifespan) để bắt tín hiệu SIGTERM, đợi các `_in_flight_requests` hoàn thành trong tối đa 30s.
- **Stateless**: Ứng dụng không lưu state trong bộ nhớ cục bộ (sử dụng Redis để lưu rate limit và history nếu scale) giúp việc scale-out nhiều instance không làm mất context người dùng.

## Part 6: Final Project
- **Status**: Completed 100% requirements.
- **Tools used**: FastAPI, Docker (Multi-stage), Redis, Railway.