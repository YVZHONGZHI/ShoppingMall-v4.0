<template>
    <div class="home" v-if="isLoading">
        <nav class="navbar navbar-inverse">
            <div class="container-fluid">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <a class="navbar-brand">ATM购物商城</a>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
                    <ul class="nav navbar-nav">
                        <li class="active"><a>商品</a></li>
                        <li><a href="" @click="goPage('/vip')">精品推荐</a></li>
                    </ul>
                    <form class="navbar-form navbar-left">
                        <div class="form-group">
                            <label for="search"></label>
                            <input type="text" id="search" class="form-control" placeholder="输入关键字" v-model="search">&nbsp;
                        </div>
                        <input type="button" class="btn btn-default" value="搜索" @click="test">
                    </form>
                    <ul class="nav navbar-nav navbar-right">
                        <li v-if="token"><a>{{ username }}</a></li>
                        <li class="dropdown" v-if="token">
                            <a class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">更多操作 <span class="caret"></span></a>
                            <ul class="dropdown-menu">
                                <li><a href="" data-toggle="modal" data-target=".bs-example-modal-lg">修改密码</a></li>
                                <li><a href="" data-toggle="modal" data-target=".bs-example-modal-sm">修改头像</a></li>
                                <li><a href="" @click="goPage('/backend')">后台管理</a></li>
                                <li role="separator" class="divider"></li>
                                <li><a href="" @click="logout">退出登录</a></li>
                            </ul>
                            <SetPassword/>
                            <SetAvatar/>
                        </li>
                        <li v-if="!token"><a href="" @click="goPage('/register')">注册</a></li>
                        <li v-if="!token"><a href="" @click="goPage('/login')">登录</a></li>
                    </ul>
                </div><!-- /.navbar-collapse -->
            </div><!-- /.container-fluid -->
        </nav>
        <div class="container-fluid">
            <div class="col-md-2">
                <div class="panel panel-primary">
                    <div class="panel-heading">
                        <h3 class="panel-title">直播</h3>
                    </div>
                    <div class="panel-body">
                        点击观看华为p60 发布会
                    </div>
                </div>
                <div class="panel panel-danger">
                    <div class="panel-heading">
                        <h3 class="panel-title">想换新手机了怎么办?</h3>
                    </div>
                    <div class="panel-body">
                        多家线下门店推出以旧换新业务
                    </div>
                </div>
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h3 class="panel-title">突发</h3>
                    </div>
                    <div class="panel-body">
                        手机发烫的原因竟然是...
                    </div>
                </div>
            </div>
            <div class="col-md-8">
                <ul class="media-list" v-for="goods_obj in goods_queryset">
                    <li class="media">
                        <h4 class="media-heading">
                            <a :href="'/goods/' + goods_obj.id">
                                {{ goods_obj.shop_name }}
                            </a>
                        </h4>
                        <div class="media-left">
                            <img class="media-object" :src="goods_obj.shop_picture" width="125" height="125" alt="商品图片">
                        </div>
                        <div class="media-body" style='white-space:pre-wrap'>{{ goods_obj.desc }}</div>
                        <div>
                            <br>
                            <span>发售于&nbsp;&nbsp;</span>
                            <span>
                                {{ goods_obj.create_time }}&nbsp;&nbsp;
                            </span>
                            <span>
                                <span class="glyphicon glyphicon-comment"></span>评论({{ goods_obj.comment_num }})&nbsp;&nbsp;
                            </span>
                            <span>
                                <span class="glyphicon glyphicon-thumbs-up"></span>点赞({{ goods_obj.up_num }})
                            </span>
                        </div>
                    </li>
                    <hr>
                </ul>
            </div>
            <div class="col-md-2">
                <div class="panel panel-primary">
                    <div class="panel-heading">
                        <h3 class="panel-title">广告标题</h3>
                    </div>
                    <div class="panel-body">
                        广告内容
                    </div>
                </div>
                <div class="panel panel-danger">
                    <div class="panel-heading">
                        <h3 class="panel-title">广告标题</h3>
                    </div>
                    <div class="panel-body">
                        广告内容
                    </div>
                </div>
                <div class="panel panel-info">
                    <div class="panel-heading">
                        <h3 class="panel-title">广告标题</h3>
                    </div>
                    <div class="panel-body">
                        广告内容
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
    import SetAvatar from "../components/SetAvatar";
    import SetPassword from "../components/SetPassword";
    export default {
        name: "Home",
        data() {
            return {
                username: '',
                goods_queryset: [],
                search: '',
                token: '',
                isLoading: false
            }
        },
        created() {
            this.username = this.$cookies.get('username')
            this.token = this.$cookies.get('token')
            this.$axios.get(this.$settings.base_url+'/home/').then(response => {
                this.goods_queryset = response.data
                this.isLoading = true
            })
        },
        methods: {
            logout() {
                this.$cookies.remove('username')
                this.$cookies.remove('token')
                this.username = ''
                this.token = ''
            },
            test() {
                if (this.search) {
                    this.$router.push('/search/?search=' + this.search)
                    this.search = ''
                }
                else{
                    alert("关键字不能为空!")
                }
            },
            goPage(url_path) {
                this.$router.push(url_path)
            }
        },
        components: {
            SetPassword,
            SetAvatar
        }
    }
</script>


<style lang="less" scoped>
    @import '~bootstrap/less/bootstrap.less';

    .home {
        font-size: 14px;
        line-height: 1.42857143;
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
</style>