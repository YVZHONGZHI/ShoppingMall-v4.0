<template>
    <div class="pay">
        <p>支付成功！</p>
        <p><b>订单号：</b>{{ order.out_trade_no }}</p>
        <p><b>交易号：</b>{{ order.trade_no }}</p>
        <p><b>付款时间：</b>{{ order.timestamp }}</p>
        <p><a href="" @click="goPage('/home')">返回网站首页</a></p>
    </div>
</template>


<script>
    export default {
        name: "Pay",
        data() {
            return {order: {}}
        },
        created() {
            let params = location.search.substring(1)
            let items = params.length ? params.split('&') : []
            for (let i = 0; i < items.length; i++) {
                let w = items[i].split('=')
                if (w.length >= 2) {
                    let w1 = decodeURIComponent(w[0])
                    this.order[w1] = decodeURIComponent(w[1])
                }
            }
            this.$axios.put(this.$settings.base_url+'/success/'+this.order.out_trade_no+'/', {
                trade_no: this.order.trade_no,
                pay_time: this.order.timestamp
            })
        },
        methods: {
            goPage(url_path) {
                this.$router.push(url_path)
            }
        }
    }
</script>


<style scoped>
    .pay {
        padding: 10px;
        font-size: 14px;
        max-width: 550px;
        min-height: 200px;
        margin: 8% auto 0;
    }

    p {
        color: #555;
        margin: 10px 10px;
    }
</style>