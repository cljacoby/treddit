<template>
    <div id="submission"
        v-bind:class="{ deleting: isDeleting }">
        <div id="submissionLeft" class="submissionMember"></div>
        <div id="submissionMiddle" class="submissionMember">{{ url }}</div>   
        <div id="submissionRight" class="submissionMember">{{ refreshes }}</div>   
    </div>
</template>

<script>
export default {
    name: "Submission",
    props: {
    },
    data: function() {
        return {
            url: null,
            refreshes: 0,
            isDeleting: true,
        }
    },
    methods: {
        test: async function() {
            let resp = await fetch("http://www.google.com");
            let myJson = await response.json();
            console.log(JSON.stringify(myJson));
        },
    }
}
</script>

<style scoped>

#submission {
    display: flex;
    flex-wrap: nowrap;
    padding: 10px;
}

#submission.deleting {
    /*background-color: red;*/
}

.submissionMember {
    border: 1px solid;
    border-color: var(--gbl-clr-grey);
    /* Width 100 here mostly builds out the wireframe; consider removing later */
    width: 100%;

    margin-right: 10px;
}

#submissionLeft {
    flex-basis: 15%;
    background-color: red;
}

#submissionLeft:hover {
    background-color: darkred;
    cursor: pointer;
}

#submissionLeft:active {
    background-color: maroon;
}

#submissionRight {
}

#submissionMiddle {
}


</style>
