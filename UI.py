class SelfAPI {
    constructor() {
        this.status = "in progress";
    }

    async fetchData() {
        //make api call and update the status
        this.status = await API.fetchData();
        return this.status;
    }

    render() {
        //update the dom with the status
        document.getElementById("status").innerHTML = this.status;
    }
}

const selfApi = new SelfAPI();