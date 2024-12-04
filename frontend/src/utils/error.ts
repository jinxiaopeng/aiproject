export const handleApiError = (error: any, defaultMessage = '操作失败') => {
  console.error('API error:', error)
  if (error.response?.data) {
    return error.response.data.detail || 
           error.response.data.message || 
           defaultMessage
  }
  return error.message || defaultMessage
} 