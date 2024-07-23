<template>
  <body class="blackground" data-spy="scroll" data-target="#navigation">
  
    <div id="wrap">
      <div class="row">
       <!-- 上边栏 -->
        <div class="navbar navbar-default navbar-fixed-top navbar-transparent-black " style="height:60px" role="navigation"
                 id="navbar">
    
                 <el-header>
                  <div>
                    <img src="../assets/header1.jpeg" >
                    <span style="color: black">合作网络分析系统</span>
                  </div>
                <el-button type="info" @click="logout">退出</el-button> 
                </el-header>
             
               

        
        </div>
      <!-- 上边栏 -->
     
        <div style="margin-top:70px">            
             
                  <router-view >  </router-view>
                        
               
        </div>

      </div>
    </div>
  </body>
   
      

    
  
    
    

</template>

<script>
export default {
   name: 'home',
   data(){
     return {
       attr :[],
       isCollapse:false,
       activePath : '',
       input:'',
       paper:0,
       author:0,
       institution:0,
     }
   },
  
   methods: {
      
       logout(){
           window.sessionStorage.clear()
           this.$router.push('/login')

       }

       
   }
}
</script>
<style lang="less" scoped>
.home-container{
   height: 100%;
}


.el-header{
  
   display: flex;
   justify-content: space-between;
   padding-left: 0;
   align-items: center;
   color: #fff;
   font-size: 20px;
   > div {
       display: flex;
       align-items: center;
       span {
           margin-left: 15px;
       }
       img {
           margin-left: 15px;
           width: 60px;
           height: 60px;
           border-radius:50%;
           background-color:#eee;
       }

      
   }

}

.el-main{
   background-color:  #E9EEF3;
}



</style>