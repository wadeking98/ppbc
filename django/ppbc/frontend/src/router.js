import Vue from 'vue';
import Router from 'vue-router';
import Home from './views/Home.vue';
import Welcome from './views/Welcome.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/home',
      name: 'home',
      component: Home
    },
    {
      path: '/',
      name: 'login',
      component: Welcome
    },
    {
      path: '/signin',
      name: 'signin',
      component: () => import('./views/Signin.vue'),
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('./views/Signup.vue'),
    },
    {
      path: '/connections',
      name: 'connections',
      component: () => import('./views/Conn.vue'),
    },
    {
      path: '/messages/:conn_id',
      name: 'messages',
      component: () => import('./views/Mess.vue'),
    },
    {
      path: '/credentials/:conn_id',
      name: 'credentials',
      component: () => import('./views/Cred.vue'),
    },
    {
      path: '/out_requests/:conn_id',
      name: 'out_requests',
      component:() => import('./views/OutReq.vue'),
    },
    {
      path: '/in_requests/:conn_id',
      name: 'in_requests',
      component:() => import('./views/InReq.vue')
    },
    {
      path: '/profile',
      name: 'profile',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Profile.vue'),
    },
    {
      path: '/medications',
      name: 'medications',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Medications.vue'),
    },
    {
      path: '/immunizations',
      name: 'immunizations',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/Immunizations.vue'),
    },
    {
      path: '/lab-results',
      name: 'lab-results',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import(/* webpackChunkName: "about" */ './views/LabResults.vue'),
    },
  ],
});
