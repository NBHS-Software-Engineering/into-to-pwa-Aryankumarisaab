// PWA Installation and Service Worker Registration
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/static/js/serviceworker.js')
      .then(function(registration) {
        console.log('ServiceWorker registration successful with scope: ', registration.scope);
        
        // Check for updates
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          console.log('ServiceWorker update found!');
          
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              console.log('New content is available; please refresh.');
              showUpdateNotification();
            }
          });
        });
      })
      .catch(function(error) {
        console.log('ServiceWorker registration failed: ', error);
      });
  });

  // Listen for claiming of service worker
  let refreshing = false;
  navigator.serviceWorker.addEventListener('controllerchange', () => {
    if (!refreshing) {
      window.location.reload();
      refreshing = true;
    }
  });
}

// PWA Install Prompt
let deferredPrompt;
const installButton = document.createElement('button');

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent the mini-infobar from appearing on mobile
  e.preventDefault();
  // Stash the event so it can be triggered later
  deferredPrompt = e;
  // Show custom install button if needed
  showInstallPromotion();
});

function showInstallPromotion() {
  console.log('PWA install available');
  // You could show a custom install button here
  // For now, we'll just log it
}

function showUpdateNotification() {
  // Create a simple update notification
  const notification = document.createElement('div');
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: #14e6dd;
    color: #0f1419;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 1000;
    font-weight: 600;
  `;
  notification.innerHTML = `
    <p>New version available!</p>
    <button onclick="this.parentElement.remove(); location.reload();" 
            style="background: #0f1419; color: #14e6dd; border: none; padding: 0.5rem 1rem; border-radius: 4px; cursor: pointer; margin-top: 0.5rem;">
      Refresh
    </button>
  `;
  document.body.appendChild(notification);
}

// Install PWA function
async function installPWA() {
  if (deferredPrompt) {
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to the install prompt: ${outcome}`);
    deferredPrompt = null;
  }
}

// Network status detection
window.addEventListener('online', function() {
  console.log('App is online');
  showNetworkStatus('You are back online!', 'success');
});

window.addEventListener('offline', function() {
  console.log('App is offline');
  showNetworkStatus('You are currently offline. Some features may not work.', 'warning');
});

function showNetworkStatus(message, type) {
  const statusDiv = document.createElement('div');
  statusDiv.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    padding: 1rem 2rem;
    border-radius: 8px;
    color: white;
    font-weight: 600;
    z-index: 1000;
    background: ${type === 'success' ? '#00d26a' : '#ff9500'};
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  `;
  statusDiv.textContent = message;
  document.body.appendChild(statusDiv);
  
  setTimeout(() => {
    statusDiv.remove();
  }, 3000);
}

// Enhanced watchlist functionality
async function addToWatchlist(itemId, itemType) {
  // Show loading state
  const button = event.target;
  const originalText = button.textContent;
  button.textContent = 'Adding...';
  button.disabled = true;

  try {
    const response = await fetch('/add_to_watchlist', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        item_id: itemId,
        item_type: itemType
      })
    });
    
    const result = await response.json();
    
    if (result.success) {
      showNotification('Added to watchlist! 🎉', 'success');
      // Update button state
      button.textContent = '✓ In Watchlist';
      button.style.background = '#00d26a';
      button.onclick = null;
    } else {
      showNotification('Already in watchlist!', 'info');
      button.textContent = '✓ In Watchlist';
      button.style.background = '#00d26a';
      button.onclick = null;
    }
  } catch (error) {
    console.error('Error adding to watchlist:', error);
    
    if (!navigator.onLine) {
      showNotification('You are offline. Added to local queue.', 'warning');
      // Store in localStorage for sync when online
      queueOfflineAction('addToWatchlist', { itemId, itemType });
    } else {
      showNotification('Error adding to watchlist', 'error');
    }
    
    // Reset button
    button.textContent = originalText;
    button.disabled = false;
  }
}

function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  const colors = {
    success: '#00d26a',
    error: '#ff4757',
    warning: '#ff9500',
    info: '#14e6dd'
  };
  
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${colors[type]};
    color: white;
    padding: 1rem 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    z-index: 1000;
    font-weight: 600;
    transform: translateX(100%);
    transition: transform 0.3s ease;
  `;
  notification.textContent = message;
  document.body.appendChild(notification);
  
  // Animate in
  setTimeout(() => {
    notification.style.transform = 'translateX(0)';
  }, 100);
  
  // Auto remove after 3 seconds
  setTimeout(() => {
    notification.style.transform = 'translateX(100%)';
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 3000);
}

// Offline action queue
function queueOfflineAction(action, data) {
  const queue = JSON.parse(localStorage.getItem('offlineActions') || '[]');
  queue.push({ action, data, timestamp: Date.now() });
  localStorage.setItem('offlineActions', JSON.stringify(queue));
}

// Sync offline actions when back online
window.addEventListener('online', async () => {
  const queue = JSON.parse(localStorage.getItem('offlineActions') || '[]');
  if (queue.length > 0) {
    console.log('Syncing offline actions...');
    
    for (const item of queue) {
      try {
        if (item.action === 'addToWatchlist') {
          await addToWatchlist(item.data.itemId, item.data.itemType);
        }
      } catch (error) {
        console.error('Failed to sync action:', error);
      }
    }
    
    // Clear the queue
    localStorage.removeItem('offlineActions');
    showNotification('Offline actions synced!', 'success');
  }
});

// Performance monitoring
window.addEventListener('load', () => {
  // Log performance metrics
  if ('performance' in window) {
    const perfData = window.performance.timing;
    const loadTime = perfData.loadEventEnd - perfData.navigationStart;
    console.log(`Page load time: ${loadTime}ms`);
    
    if (loadTime > 3000) {
      console.warn('Page load time is slow. Consider optimizing assets.');
    }
  }
});

// Add to global scope for HTML onclick handlers
window.addToWatchlist = addToWatchlist;
window.installPWA = installPWA;