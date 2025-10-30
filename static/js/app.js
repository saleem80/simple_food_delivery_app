$(document).ready(function() {
    // Auto-refresh functionality for dashboards
    const currentPage = window.location.pathname;
    
    // Auto-refresh booking statuses every 30 seconds on dashboard pages
    if (currentPage.includes('dashboard') || currentPage === '/') {
        setInterval(function() {
            // Only refresh if user is not currently typing or interacting
            if (!$('input:focus, textarea:focus, select:focus').length) {
                location.reload();
            }
        }, 30000); // 30 seconds
    }
    
    // Enhanced form validation
    $('form').on('submit', function(e) {
        const form = $(this);
        const submitBtn = form.find('button[type="submit"]');
        
        // Disable submit button to prevent double submission
        submitBtn.prop('disabled', true).text('Processing...');
        
        // Re-enable after 3 seconds as fallback
        setTimeout(function() {
            submitBtn.prop('disabled', false).text(submitBtn.data('original-text') || 'Submit');
        }, 3000);
    });
    
    // Store original button text
    $('button[type="submit"]').each(function() {
        $(this).data('original-text', $(this).text());
    });
    
    // Enhanced booking status updates
    $('.update-status').on('click', function(e) {
        e.preventDefault();
        const button = $(this);
        const bookingId = button.data('booking-id');
        const newStatus = button.data('status');
        const originalText = button.text();
        
        button.prop('disabled', true).text('Updating...');
        
        $.ajax({
            url: '/bookings/update-status/',
            method: 'POST',
            data: JSON.stringify({
                booking_id: bookingId,
                status: newStatus
            }),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                if (response.success) {
                    showNotification('Status updated successfully!', 'success');
                    setTimeout(() => location.reload(), 1000);
                } else {
                    showNotification('Error: ' + response.error, 'error');
                    button.prop('disabled', false).text(originalText);
                }
            },
            error: function() {
                showNotification('Network error. Please try again.', 'error');
                button.prop('disabled', false).text(originalText);
            }
        });
    });
    
    // Enhanced booking assignment
    $('.assign-delivery-partner').on('change', function() {
        const select = $(this);
        const bookingId = select.data('booking-id');
        const deliveryPartnerId = select.val();
        
        if (deliveryPartnerId) {
            const partnerName = select.find('option:selected').text();
            
            if (confirm(`Assign this booking to ${partnerName}?`)) {
                select.prop('disabled', true);
                
                $.ajax({
                    url: '/bookings/assign/',
                    method: 'POST',
                    data: JSON.stringify({
                        booking_id: bookingId,
                        delivery_partner_id: deliveryPartnerId
                    }),
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val()
                    },
                    success: function(response) {
                        if (response.success) {
                            showNotification('Booking assigned successfully!', 'success');
                            setTimeout(() => location.reload(), 1000);
                        } else {
                            showNotification('Error: ' + response.error, 'error');
                            select.prop('disabled', false).val('');
                        }
                    },
                    error: function() {
                        showNotification('Network error. Please try again.', 'error');
                        select.prop('disabled', false).val('');
                    }
                });
            } else {
                select.val('');
            }
        }
    });
    
    // Real-time notifications
    function showNotification(message, type) {
        const notification = $(`
            <div class="alert alert-${type} notification" style="
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 1000;
                min-width: 300px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            ">
                ${message}
                <button type="button" class="close" style="float: right; margin-left: 10px;">&times;</button>
            </div>
        `);
        
        $('body').append(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => notification.fadeOut(() => notification.remove()), 5000);
        
        // Manual close
        notification.find('.close').on('click', () => {
            notification.fadeOut(() => notification.remove());
        });
    }
    
    // Enhanced chat functionality
    if ($('#chat-messages').length) {
        const chatMessages = $('#chat-messages');
        const messageInput = $('#chat-message-input');
        
        // Auto-resize textarea
        messageInput.on('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Character counter
        messageInput.after('<small class="text-muted char-counter">0/500</small>');
        messageInput.on('input', function() {
            const count = $(this).val().length;
            $('.char-counter').text(`${count}/500`);
            
            if (count > 450) {
                $('.char-counter').addClass('text-warning');
            } else {
                $('.char-counter').removeClass('text-warning');
            }
        });
        
        // Scroll to bottom on new messages
        function scrollToBottom() {
            chatMessages.scrollTop(chatMessages[0].scrollHeight);
        }
        
        // Enhanced message display
        function formatTimestamp(timestamp) {
            const date = new Date(timestamp);
            const now = new Date();
            const diff = now - date;
            
            if (diff < 60000) { // Less than 1 minute
                return 'Just now';
            } else if (diff < 3600000) { // Less than 1 hour
                return Math.floor(diff / 60000) + 'm ago';
            } else if (date.toDateString() === now.toDateString()) {
                return date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            } else {
                return date.toLocaleDateString();
            }
        }
        
        // Update timestamps every minute
        setInterval(function() {
            $('.message-meta').each(function() {
                const meta = $(this).text();
                const parts = meta.split(' • ');
                if (parts.length === 2) {
                    const timestamp = $(this).data('timestamp');
                    if (timestamp) {
                        $(this).text(parts[0] + ' • ' + formatTimestamp(timestamp));
                    }
                }
            });
        }, 60000);
    }
    
    // Form field enhancements
    $('.form-control').on('focus', function() {
        $(this).closest('.form-group').addClass('focused');
    }).on('blur', function() {
        $(this).closest('.form-group').removeClass('focused');
    });
    
    // Mobile number formatting
    $('input[type="tel"], input[name*="phone"], input[name*="mobile"]').on('input', function() {
        let value = $(this).val().replace(/\D/g, ''); // Remove non-digits
        if (value.length > 10) {
            value = value.substring(0, 10); // Limit to 10 digits
        }
        $(this).val(value);
    });
    
    // Price formatting
    $('input[name*="price"], input[type="number"][step="0.01"]').on('input', function() {
        let value = parseFloat($(this).val());
        if (!isNaN(value)) {
            $(this).val(value.toFixed(2));
        }
    });
    
    // Enhanced table interactions
    $('.table tbody tr').on('click', function() {
        if (!$(this).hasClass('no-click')) {
            $(this).addClass('table-active');
            setTimeout(() => $(this).removeClass('table-active'), 200);
        }
    });
    
    // Loading states for AJAX calls
    $(document).ajaxStart(function() {
        $('body').addClass('loading');
    }).ajaxStop(function() {
        $('body').removeClass('loading');
    });
    
    // Confirmation dialogs for dangerous actions
    $('a[href*="cancel"], button:contains("Cancel"), button:contains("Delete")').on('click', function(e) {
        if (!confirm('Are you sure you want to proceed?')) {
            e.preventDefault();
        }
    });
    
    // Auto-focus first input field
    $('.form-control:first').focus();
    
    // Enhanced responsive behavior
    function updateLayout() {
        if ($(window).width() < 768) {
            $('.table').addClass('table-sm');
            $('.card').addClass('card-sm');
        } else {
            $('.table').removeClass('table-sm');
            $('.card').removeClass('card-sm');
        }
    }
    
    $(window).on('resize', updateLayout);
    updateLayout();
});

// Service Worker for offline support (basic)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/sw.js').then(function(registration) {
            console.log('SW registered: ', registration);
        }, function(registrationError) {
            console.log('SW registration failed: ', registrationError);
        });
    });
}