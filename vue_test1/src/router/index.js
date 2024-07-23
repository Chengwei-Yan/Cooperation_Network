import Vue from 'vue'
import Router from 'vue-router'

import Login from '@/components/Login.vue'
import home from '@/components/home.vue'
import welcome from '@/components/welcome.vue'
import user from '@/components/user.vue'
import upload from '@/components/upload.vue'
import key from '@/components/key.vue'
import title from '@/components/title.vue'
import detail from '@/components/detail.vue'
import display from '@/components/display.vue'
import display_country from '@/components/display_country.vue'

Vue.use(Router)

// export default new Router({
//   mode: 'history',
//   routes: [
//     {
//       path: '/' ,redirect:'/login'
//     },
   
//     {
//       path: '/login',
//       name: 'Login',
//       component: Login

//     },
//     {
//       path:'/home',
//       name:'home',
//       component: home

//     }
//   ]
// })
const router =  new Router({
  mode: 'history',
  routes: [
    {
      path: '/' ,redirect:'/login'
    },
   
    {
      path: '/login',
      name: 'Login',
      component: Login

    },
    {
      path:'/home',
      name:'home',
      component: home,
      children:[{
        path:'/welcome',
        name:'welcome',
        component:welcome
      },{
        path:'/user',
        name:'user',
        component:user

      },{
        path:'/upload',
        name:'upload',
        component:upload

      },{
        path:'/key',
        name:'key',
        component:key

      },{
        path:'/title',
        name:'title',
        component:title

      },
      {
        path: '/detail',
        name: 'detail',
        component: detail
  
      },
      {
        path: '/display',
        name: 'display',
        component: display
  
      },
      {
        path: '/display_country',
        name: 'display_country',
        component: display_country
  
      },
     ],
      redirect:'/user'

    },
    
  ]
})
router.beforeEach((to,from,next)=>{
  // to 将要访问的路径
  // from 从哪个路径跳转来的
  // next 表示放行
  if(to.path ==='/login') return next()
  const tokenstr = window.sessionStorage.getItem('token')
  if(!tokenstr)
    return next('/login')
  next()



})
export default router