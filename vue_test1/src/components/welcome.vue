<template>
  <div >
    
 
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item >搜索</el-breadcrumb-item>
            
        </el-breadcrumb>
          <el-card class="box-card"   >
              <el-row :gutter="20">
                <el-col :span="8" :offset="4" >
                   <el-input placeholder="请输入内容" id="key" v-model="input">
                    <el-button slot="append" icon="el-icon-search" @click="getalllist" ></el-button>
                  </el-input>
                </el-col>
                <el-col :span="2">
                  <el-dropdown>
                    <el-button  icon="el-icon-download">
                      下载<i class="el-icon-arrow-down el-icon--right"></i>
                    </el-button>
                    <el-dropdown-menu slot="dropdown" >
                      <el-dropdown-item  @click.native="download('txt')">TXT文件</el-dropdown-item>
                      <el-dropdown-item  @click.native="download('csv')">CSV文件</el-dropdown-item>
                    </el-dropdown-menu>
                   
                  </el-dropdown>
                  
                    
                </el-col>
                <el-col :span="3">
                  <el-button   icon="el-icon-picture" @click="display">
                    多层次网络视图
                  </el-button>

                </el-col>
                <el-col :span="3">
                  <el-button  icon="el-icon-picture" @click="displaycoo">
                    国际合作网络视图
                  </el-button>

                </el-col>
               
              </el-row>
          </el-card>
         
          
          <el-table
          :data="datalist"
          style="width: 100%  " 
          height="520px"
          v-loading="loading"
          >
          <el-table-column
            label="论文题目"
            prop="title"
            
            >
          </el-table-column>
          <el-table-column
            label="作者"
            prop="author"
           >
          </el-table-column>
          <el-table-column
            label="通讯作者地址"
            prop="address"
            >
          </el-table-column>
          <el-table-column
          fixed="right"
          label="操作"
          width="100">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" size="small" icon="el-icon-search"><font color="black">查看</font></el-button>
            
          </template>
        </el-table-column>
        </el-table>
        <!--  
                <template slot-scope="scope">
                  <el-button @click="handleClick(scope.row)" type="primary" size="small">查看</el-button>
                  
                </template>
                
               
                
              </el-table-column>
            </el-table>
            -->
            
          
    <el-card class="box-card"  >
        <el-pagination
        @current-change="handleCurrentChange"
        layout="total, prev, pager, next, jumper"
        :page-size="10"
        :total="total">
      </el-pagination>
        </el-card>
    
</div>

</template>


<script>
    import { baseurl } from '../setting.js'
    import { ipurl } from '../setting.js'
    export default {
        data(){
            return{
                queryInfo:{
                    query:'',
                    pagenum:1,
                    pagesize:10,
                    key:'',
                },
                datalist:[],
                detaillist:[],
                total:0,
                input:'',
                dialogTableVisible: false,
                loading:true,
               
                
            }
        },
        created(){
            this.getalllist()
        },
        methods:{
            async getalllist(){
                const search = window.sessionStorage.getItem('search')
                    if(search) {
                      this.input = search
                      window.sessionStorage.removeItem('search')
                    }
                this.loading = true
                this.queryInfo.key = this.input
                // this.queryInfo.key = document.getElementById('key').value
                const {data:res} = await this.$axios.get('search/',{params:this.queryInfo})
                this.loading = false
                if(res.status!=200) return this.$message.error('获取用户列表失败!')
                this.datalist=[]
                for (let i=0; i < res.title.length; i++) {
                    this.datalist.push({'title':res.title[i],'author':res.author[i],'address':res.address[i],'detail':[]})
                }
                this.total = res.num
                console.log(this.datalist)
            },
            handleCurrentChange(newpage){
                this.queryInfo.pagenum=newpage
                this.getalllist()

            },
        
            
            
            handleClick(row){
              window['title'] = row.title
              window.open(ipurl+'detail')

            },
            // async download(choice){
            //   const loading = this.$loading({
            //     lock: true,
            //     text: 'Loading',
            //     spinner: 'el-icon-loading',
            //     background: 'rgba(0, 0, 0, 0.7)'
            //   });

            //   const {data:res} = await this.$axios.get('download/',{params:{type:choice}})
            //   loading.close()
            //   if(res.status!=200) return this.$message.error(res.data)
            //   console.log(res.data)
            //   this.$message({
            //     message: res.data,
            //     type: 'success'
            //   });


            // },
            // async download(choice){
            //   const loading = this.$loading({
            //     lock: true,
            //     text: 'Loading',
            //     spinner: 'el-icon-loading',
            //     background: 'rgba(0, 0, 0, 0.7)'
            //   });

            //   const {data:res} = await this.$axios.get('download/',{params:{type:choice}})
            //   loading.close()
            //   if(res.status!=200) return this.$message.error(res.data)
             
            //   window.open(this.$axios.defaults.baseURL+res.data)
              


            // },
            download(choice){
              const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
              });
              window.open(baseurl+`download/?type=${choice}`)
              // window.location.href = `/download/?type=${choice}`
              // this.$axios.get('download/',{params:{type:choice}})
              loading.close()
              // if(res.status!=200) return this.$message.error(res.data)
             
              


            },

            display(){
              this.$router.push('/display');

            },
            displaycoo(){
              this.$router.push('/display_country');

            }

            
        }
        
    }
</script>

<style lang="less" scoped>
/deep/ .el-table, .el-table__expanded-cell{
  background-color: transparent;
}
/* 表格内背景颜色 */
/deep/ .el-table th,
/deep/ .el-table tr,
/deep/ .el-table td {
  background-color: transparent;
}
/deep/ .el-card {
  background-color: transparent;
}
/deep/ .el-pagination {
  background-color: transparent;
}
/deep/ .el-button {
  background-color: transparent;
}


</style>



