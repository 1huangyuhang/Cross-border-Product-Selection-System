package com.project.util;

import org.springframework.util.StringUtils;

import java.util.regex.Pattern;

/**
 * 数据验证工具类
 * 按照software.md文档要求实现数据验证
 */
public class ValidationUtils {
    
    private static final Pattern EMAIL_PATTERN = Pattern.compile(
        "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
    );
    
    private static final Pattern URL_PATTERN = Pattern.compile(
        "^(https?|ftp)://[^\\s/$.?#].[^\\s]*$"
    );
    
    /**
     * 验证邮箱格式
     */
    public static boolean isValidEmail(String email) {
        if (!StringUtils.hasText(email)) {
            return false;
        }
        return EMAIL_PATTERN.matcher(email).matches();
    }
    
    /**
     * 验证URL格式
     */
    public static boolean isValidUrl(String url) {
        if (!StringUtils.hasText(url)) {
            return false;
        }
        return URL_PATTERN.matcher(url).matches();
    }
    
    /**
     * 验证价格范围
     */
    public static boolean isValidPrice(Double price) {
        return price != null && price >= 0 && price <= 999999.99;
    }
    
    /**
     * 验证评分范围
     */
    public static boolean isValidRating(Double rating) {
        return rating != null && rating >= 0.0 && rating <= 5.0;
    }
    
    /**
     * 验证字符串长度
     */
    public static boolean isValidStringLength(String str, int maxLength) {
        return str == null || str.length() <= maxLength;
    }
    
    /**
     * 验证必填字段
     */
    public static boolean isRequiredField(String field) {
        return StringUtils.hasText(field);
    }
}
