<template>
    <div>
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item >详细信息</el-breadcrumb-item>
            
        </el-breadcrumb>
        <el-table
            :data="datalist"
            height="700px"
            border
            style="width: 100%"  >
            <el-table-column
            prop="attr"
            label="属性"
            >
            </el-table-column>
            <el-table-column
            prop="value"
            label="内容"
            >
            </el-table-column>
           
        </el-table>
    </div>
</template>

<script>
    export default {
        data(){
            return{
                
                datalist:[],
            }
        },
        created(){
            this.getDetailList()
        },
        methods:{
            async getDetailList(){
                console.log( window.opener['title'])
                const {data:res} = await this.$axios.get('datadetail/',{params:{query:'',title: window.opener['title']}})
                if(res.status!=200) return this.$message.error('获取用户列表失败!')
                this.datalist=[]
                for (let i=0; i < res.value.length; i++) {
                    this.datalist.push({'attr':res.attr[i],'value':res.value[i]})
                }
                console.log(this.datalist)
            },
           
            
           
            

            
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
</style>