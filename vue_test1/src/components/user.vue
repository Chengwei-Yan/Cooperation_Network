<template>

   <!-- cards -->
<div id="content" class="col-md-12" style="margin-top: 200px; " >
    
    <section  class="tile transparent" style=" margin-right:250px" >
        <div class="tile-widget color transparent-black textured">
            <div class="table-responsive" align="center">
   <div class="row cards" style="margin-top: 50px;">

    <el-row :gutter="20"  >
        <el-col :span="8" :offset="8" align-items="center">
          
           <el-input placeholder="请输入查询关键词,如:industrial biotechnology"  v-model="input"  >
            <el-button slot="append" icon="el-icon-search" @click="getalllist" ></el-button>
          </el-input>
        </el-col>
        
    </el-row>

    <div class="card-container col-lg-4 col-sm-6 col-sm-12" style="margin-top: 50px;">
        <div class="card card-redbrown hover">
            <div class="front">

                <div class="media">
      <span class="pull-left">
        <h1><i class="el-icon-user"></i></h1>
      </span>

                    <div class="media-body">
                        <small>作者总数</small>
                        <h2 class="media-heading animate-number" 
                            >{{ author }}</h2>
                    </div>
                </div>

                

            </div>
            
        </div>
    </div>


    <div class="card-container col-lg-4 col-sm-6 col-sm-12" style="margin-top: 50px;">
        <div class="card card-blue hover">
            <div class="front">

                <div class="media">
      <span class="pull-left">
        <h1><i class="el-icon-document"></i></h1>
      </span>

                    <div class="media-body">
                        <small>论文总数</small>
                        <h2 class="media-heading animate-number" data-value="62988"
                            data-animation-duration="1500">{{ paper }}</h2>
                    </div>
                </div>

               

            </div>
            
        </div>
    </div>


    <div class="card-container col-lg-4 col-sm-6 col-sm-12" style="margin-top: 50px;">
        <div class="card card-greensea hover">
            <div class="front">

                <div class="media">
      <span class="pull-left">
        <h1><i class="el-icon-office-building"></i></h1>
      </span>

                    <div class="media-body">
                        <small>机构总数</small>
                        <h2 class="media-heading animate-number" data-value="100%"
                            data-animation-duration="1500">{{ institution }}</h2>
                    </div>
                </div>

              

            </div>
           
        </div>
    </div>



</div>
        
            </div >
        </div >
    </section >
</div>

</template>

<script>
export default {
   name: 'user',
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
   created() {

          this.statistics()
          //  this.activePath = window.sessionStorage.getItem('activatePath')
       },
   methods: {
      
       logout(){
           window.sessionStorage.clear()
           this.$router.push('/login')

       },
       getalllist(){
        window.sessionStorage.setItem('search',this.input);
        this.$router.push('/welcome');

       },
       async statistics(){
        const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
          });

            const {data:res} = await this.$axios.get('statistics/')
            loading.close()
            if(res.status!=200) return this.$message.error(res.data)
            this.paper =res.data.paper
            this.author =res.data.author
            this.institution =res.data.institution
            
            
            


       }

       
   }
}

</script>

<style lang="less" scoped>

.sterm{
  position:relative;
  left: 50%;
  top: 40%;
  transform: translate(-50%,-50%);
  

}
.display{
  padding: 0 9px;
   margin-top: 100px;
  .statistics{
      color: white;
      height: 100px;
      border-radius:4px;
      padding: 0 8px;
      .title{
          display: flex; // 弹性布局
          justify-content: space-between; // 两边对齐
          align-items: center; // 垂直居中
      }
      p{
          font-size: 13px;
          font-weight: bold;
      }
      .num{
          font-size: 20px;
          font-weight: bold;
          text-align: center;
      }
      .tip{
          font-size: 12px;
      }
  }
}


.imgsearch{
  position: relative;
  left:50% ;
  transform: translate(-50%,0%);
  width: 100px;
  height: 100px;
  border-radius:200px;
  
  box-shadow:  0 0 5px 5px rgb(63, 6, 132);

}


</style>