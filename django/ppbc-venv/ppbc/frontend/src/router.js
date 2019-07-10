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
