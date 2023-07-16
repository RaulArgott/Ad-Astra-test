<template>
    <div class="spinner-container">
        <div class="spinner-border" role="status">
            <span class="sr-only">Loading...</span>
        </div>
    </div>
</template>
<script>
export default {
    name: 'LoadingComponent',

}
</script>
<style>
.spinner-container {
    background: rgba(43, 77, 171, 0.656);
    position: fixed;
    top: 0;
    bottom: 0;
    right: 0;
    left: 0;
}
</style>