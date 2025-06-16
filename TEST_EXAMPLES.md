# GitHub Agent - Test Examples

## 🧪 Test Cases cho Agent Intelligence

### Test Case 1: Câu đầu tiên có cả GitHub URL và PAT
**Input:**
```
Tôi muốn làm việc với GitHub repository https://github.com/owner/repository, PAT: github_pat_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Expected Behavior:**
- Agent extract URL và PAT từ câu đầu tiên
- Gọi `validate_github_url()` và `validate_github_token()` ngay lập tức
- Nếu valid, gọi `create_github_session()` luôn
- Không hỏi lại gì nữa

### Test Case 2: Câu đầu tiên chỉ có GitHub URL
**Input:**
```
Tôi muốn làm việc với repository: https://github.com/owner/repository
```

**Expected Behavior:**
- Agent extract URL và validate ngay
- Hỏi về PAT với message custom: "Tôi thấy bạn muốn làm việc với repository: https://github.com/owner/repository"
- Không hỏi lại về URL

### Test Case 3: Câu đầu tiên chỉ có PAT
**Input:**
```
PAT của tôi là: github_pat_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

**Expected Behavior:**
- Agent validate PAT trước
- Hỏi về GitHub URL

### Test Case 4: Câu đầu tiên không có thông tin
**Input:**
```
Tôi muốn làm việc với GitHub repository
```

**Expected Behavior:**
- Hỏi về GitHub URL như bình thường

## 🎯 GitHub URL Patterns cần detect:
- `https://github.com/owner/repo`
- `http://github.com/owner/repo`
- `github.com/owner/repo`
- `www.github.com/owner/repo`

## 🔑 PAT Patterns cần detect:
- `github_pat_` + 82 characters
- `ghp_` + 36 characters
- `gho_` + 36 characters
- `ghu_` + 36 characters

## ✅ Expected Results:
Với các test case trên, agent sẽ:
1. Thông minh hơn trong parse thông tin
2. Giảm số lần hỏi user
3. Tạo trải nghiệm mượt mà hơn
4. Vẫn đảm bảo validation đúng 