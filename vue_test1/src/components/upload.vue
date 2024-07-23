<template>
    <div >
        <el-breadcrumb separator-class="el-icon-arrow-right">
            <el-breadcrumb-item  :to="{ path: '/home' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item >上传</el-breadcrumb-item>
            <el-breadcrumb-item >上传论文文件</el-breadcrumb-item>
          </el-breadcrumb>
     
    <el-row :gutter="20" style="top: 50px;">
        <el-col :offset="8" :span="8">
            <el-input placeholder="输入关键词"  v-model="input" >
                <el-button slot="append" icon="el-icon-upload" @click="key" ></el-button>
            </el-input>
        </el-col>
    </el-row>
    <el-row style="top: 250px;">
        <el-col >
            <el-upload
            class="upload-demo"
            drag
            action="http://127.0.0.1:8080/getfile/"
            multiple>
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip" >只能上传web of science导出的txt文件</div>
        </el-upload>
        </el-col>
    </el-row>
    <el-row style="top: 400px;  " type="flex">
        <el-col offset="11" >
            <el-button icon="el-icon-check" @click="create">创建</el-button>
        </el-col>
        
    </el-row>
    </div>
    
</template>
<script>
 import { baseurl } from '../setting.js'
 export default {
    data(){
     return {
       input:''
     }
   },
    methods:{
    
    async create(){
        const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
          });
    const {data:res}=await this.$axios.get('create/');
    loading.close()
    if(res.status!==200)
        this.$message.error(res.data)
    else
        this.$message.success("成功创建节点");
   }
   ,
   async key(){
    const loading = this.$loading({
                lock: true,
                text: 'Loading',
                spinner: 'el-icon-loading',
                background: 'rgba(0, 0, 0, 0.7)'
          });
    const {data:res} =await this.$axios.get('insert_key/',{params:{key:this.input}})
    loading.close()
    
    if(res.status!==200)
        this.$message.error(res.data)
    else
        this.$message.success("成功上传插入主题");

   }
    }
 }
</script>
<style lang="less" scoped>

    
</style>