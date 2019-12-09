<template>
    <div id="submissionsContainer">
        <div id="addRowContainer">
            <div id="addRow" v-on:click="addRow">+</div>
        </div>
        <div id="submissions">
            <Submission v-for="(el, index) in submissions"
                class="submission submissionsMember"></Submission>
        </div>
    </div>
</template>

<script>
import Vue from 'vue'
import Submission from './Submission.vue';
import axios from "axios";

export default {
    name: "Submissions",
    components: {
        Submission,
    },
    props: [],
    data: function() {
        return {
            submissions: [],
        };
    },
    computed: {
        // In the actual implementation I dont think id need this 
        submissionsCount: function() {
            return this.submissions.length;
        }
    },
    methods: {
        addRow: function(event) {
            this.test();
            this.submissions.push(this.submissionsCount);
        },
        test: function() {
            var xhr = new XMLHttpRequest();
            xhr.open("GET", "http://rest.learncode.academy/api/vue-5/friends");
            xhr.onreadystatechange = function(arg) {
                console.log(arg);
            }
            xhr.send();
        },
    }
}
</script>

<style scoped>

#submissionsContainer {
    border: 1px solid;
    border-color: var(--gbl-clr-grey);
    display: flex;
    flex-wrap: nowrap;
    flex-direction: column;
    padding: 10px;
}

.submissionsMember {
    border: 1px solid;
    border-color: var(--gbl-clr-grey);
    margin: 10px 5px;
}

#addRowContainer {
    display: flex;
    align-items: center;
    justify-content: center;
}

#addRow {
    padding: 8px 16px !important;
    font-size: 24px !important;
    border: 1px solid transparent;
    color: white;
    border-radius: 50%;
    background-color: var(--gbl-clr-purple);
    cursor: pointer;
    user-select: none;
}

#addRow:hover {
    background-color: var(--gbl-clr-purple-darker);
}

#addRow:active {
    background-color: var(--gbl-clr-purple-darkest);
}

.submission {
}

</style>
