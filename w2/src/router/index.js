import Vue from 'vue'
import VueRouter from 'vue-router'
import Vip from '../views/Vip.vue'
import Pay from '../views/Pay.vue'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Search from '../views/Search.vue'
import Errors from '../views/Errors.vue'
import Exhibit from '../views/Exhibit.vue'
import Register from '../views/Register.vue'
import Backend from '../views/backend/Backend.vue'
import GoodsDetail from '../views/GoodsDetail.vue'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        name: 'Created',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/home',
        name: 'Home',
        component: Home
    },
    {
        path: '/vip',
        name: 'Vip',
        component: Vip
    },
    {
        path: '/exhibit',
        name: 'Exhibit',
        component: Exhibit
    },
    {
        path: '/search',
        name: 'Search',
        component: Search
    },
    {
        path: '/search/category/:category_id',
        name: 'SearchCategory',
        component: Search
    },
    {
        path: '/search/tag/:tag_id',
        name: 'SearchTag',
        component: Search
    },
    {
        path: '/goods/:goods_id',
        name: 'GoodsDetail',
        component: GoodsDetail
    },
    {
        path: '/backend',
        name: 'Backend',
        component: Backend
    },
    {
        path: '/pay/success',
        name: 'Pay',
        component: Pay
    },
    {
        path: '*',
        name: 'Errors',
        component: Errors
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router