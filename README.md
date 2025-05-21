# Barrier Page with Admin Dashboard

This application creates a barrier page that collects comprehensive user information before redirecting to Google. It includes a secure admin dashboard with a matrix/hacker theme for viewing and analyzing the collected data.

## Features

### Barrier Page
- Appears blank to users with a simple message about unsuccessful access
- Collects extensive user information in the background:
  - IP address and network details
  - Browser and OS information
  - Device specifications
  - Geolocation data
  - Hardware details
  - Browser capabilities
  - Various fingerprinting data

### Admin Dashboard
- Matrix/hacker-themed interface
- Password protected (credentials below)
- Comprehensive analytics with charts and graphs
- Detailed visitor profiles
- Data export functionality (CSV, Excel, JSON)
- Search and filtering capabilities

### Security Features
- Password protection for admin access
- Rate limiting to prevent brute force attacks
- Session timeout for enhanced security
- Input validation to prevent SQL injection
- Secure database storage

## Access Information

### Barrier Page URL
- URL: https://5000-i0eyk91ub129px7e2ffxj-5203bc7b.manusvm.computer/

### Admin Dashboard
- URL: https://5000-i0eyk91ub129px7e2ffxj-5203bc7b.manusvm.computer/admin/login
- Username: `admin`
- Password: `admin123`

## Security Recommendations

1. **Change Default Credentials**: For production use, change the default admin username and password
2. **Enable HTTPS**: For production deployment, ensure HTTPS is enabled
3. **Regular Backups**: Implement regular database backups
4. **Update Dependencies**: Keep all dependencies updated to patch security vulnerabilities
5. **Access Logs**: Monitor access logs for suspicious activities

## Technical Details

- Built with Flask (Python web framework)
- Uses SQLAlchemy for database operations
- Client-side data collection with JavaScript
- Responsive design for all device types
- Chart.js for data visualization

## Limitations

- MAC address collection is not possible via web technologies due to browser security restrictions
- Some device IDs may not be accessible depending on browser privacy settings
- Geolocation accuracy depends on user permission and device capabilities
