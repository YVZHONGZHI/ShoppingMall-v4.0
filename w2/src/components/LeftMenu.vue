<template>
    <div class="left_menu">
        <div class="panel panel-primary">
            <div class="panel-heading">
                <h3 class="panel-title">商品分类</h3>
            </div>
            <div class="panel-body">
                <p v-for="category in category_list">
                    <a :href="'/search/category/' + category.id">
                        {{ category.name }}({{ category.count_num }})
                    </a>
                </p>
            </div>
        </div>
        <div class="panel panel-danger">
            <div class="panel-heading">
                <h3 class="panel-title">商品标签</h3>
            </div>
            <div class="panel-body">
                <p v-for="tag in tag_list">
                    <a :href="'/search/tag/' + tag.id">
                        {{ tag.name }}({{ tag.count_num }})
                    </a>
                </p>
            </div>
        </div>
        <div class="panel panel-info">
            <div class="panel-heading">
                <h3 class="panel-title">日期归档</h3>
            </div>
            <div class="panel-body">
                <p v-for="date in date_list">
                    <a href="">
                        {{ date[0].split('-')[0] + '年' + date[0].split('-')[1] + '月' }}({{ date[1] }})
                    </a>
                </p>
            </div>
        </div>
    </div>
</template>


<script>
    export default {
        name: "LeftMenu",
        props: {
            date_list: []
        },
        data() {
            return {
                category_list: [],
                tag_list: []
            }
        },
        created() {
            this.$axios.get(this.$settings.base_url+'/leftmenu_category/').then(response => {
                this.category_list = response.data
            })
            this.$axios.get(this.$settings.base_url+'/leftmenu_tag/').then(response => {
                this.tag_list = response.data
            })
        }
    }
</script>


<style lang="less" scoped>
    @import '~bootstrap/less/bootstrap.less';
</style>