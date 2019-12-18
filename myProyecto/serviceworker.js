var CACHE_NAME = 'my-site-cache-v1';
var urlsToCache = [
  '/',
  '/static/core/css/estilos.css',
  '/static/core/img/logo.png',
];

self.addEventListener('install', function (event) {
  // Perform install steps
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function (cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function (event) {
  event.respondWith(

    fetch(event.request)
      .then((result) => {
        return caches.open(CACHE_NAME)
          .then(function (c) {
            c.put(event.request.url, result.clone())
            return result;
          })

      })
      .catch(function (e) {
        return caches.match(event.request)
      })



  );
});

//codigo notificacion 

importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/3.9.0/firebase-messaging.js');


var firebaseConfig = {
  apiKey: "AIzaSyBb7qXVSvPTrOpe0hkprvWVZSS6yVKNHbc",
  authDomain: "petalos-260801.firebaseapp.com",
  databaseURL: "https://petalos-260801.firebaseio.com",
  projectId: "petalos-260801",
  storageBucket: "petalos-260801.appspot.com",
  messagingSenderId: "55127486911",
  appId: "1:55127486911:web:39c36ef3d0a637bccbb10a",
  measurementId: "G-F7WRPK98P9"
};

firebase.initializeApp(firebaseConfig);
//firebase.analytics();

let messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
  console.log("ha llegado notificacion");
  
  let title = payload.Notification.title;

  let options = {
      body:payload.Notification.body,
      icon:payload.Notification.icon
  }


  self.registration.showNotification(title, options);

});