import React,{Component} from "react"
import ContestantList from "../data/contestants.json"
import Contestant from "./Contestant.js"
import CategoryList from "../data/categories.json"
import Category from './Category.js'
import Badsearch from './BadSearch.js'
import "../App.css"


class Search extends Component{
    constructor(){
        super()
        this.state = {search: "",
                    isLoading: true,
                    result: "",
                    searchType: null
                    };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleSearch = this.handleSearch.bind(this);
        this.randomPlacholder = this.randomPlacholder.bind(this);
    }
    handleSearch(searchStr){
        let terms = searchStr.trim().split(":");
        let result = ""
        let name = ""

        //With "category:" and "contestant:" keyword
        if (terms.length>1){
            let keyword = terms[0].toLowerCase();
            if (keyword==="contestant"){
                //Format text like a name (Firstname Lastname)
                terms[1] = terms[1].toLowerCase()
                    .split(' ')
                    .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                    .join(' ')
                    .trim();
                name = terms[1];
                result = ContestantList[[terms[1]]]
                this.setState({searchType: "contestant"});
            }
            if (keyword==="category"){
                //Format text like a category (ALL CAPS)
                terms[1] = terms[1].toUpperCase().trim();
                name = terms[1];
                result = CategoryList[[terms[1]]]
                this.setState({searchType: "category"});
            }
        }
        //Without "category:" and "contestant:" keyword 
        if (result===""){
            var temp1 = terms[0].toLowerCase()
                .split(' ')
                .map((s) => s.charAt(0).toUpperCase() + s.substring(1))
                .join(' ')
                .trim();
            if([temp1] in ContestantList){
                console.log("contestant!")
                name = temp1;
                result = ContestantList[[temp1]];
                this.setState({searchType: "contestant"});
            }
            else{
                console.log("category!")
                temp1 = terms[0].toUpperCase().trim();
                if([temp1] in CategoryList){
                    name = temp1;
                    result = CategoryList[[temp1]];
                    this.setState({searchType: "category"});
                }
            }
        }
        //The user inputted a meaningless value
        if (result===""){
            console.log("reached here")
            result="That's not what we were looking for.";
            this.setState({searchType: "undefined"});
        }
        console.log(result);
        return [name,result];
    }
    randomPlacholder(){
        var phrases = [
            "Make a selection...",
            "You're in command of the board now..."
        ]
        var phrase = phrases[Math.floor(Math.random() * phrases.length)];
        return phrase
    }

    handleChange(event){
        //In case someone is searching for a new term, we have to reset search query type
        if (this.state.searchType !== null){
            this.setState({isLoading: true})
        }
        this.setState({search: event.target.value});
    }
    handleSubmit() {
        this.setState({isLoading: false, result: this.handleSearch(this.state.search)})
    }
    render(){
        return(
            <div>
                <input type="text" style={{"width": 500}} value={this.state.search} onChange={this.handleChange} placeholder={this.randomPlacholder()} />
                <button type="submit" onClick={this.handleSubmit}>Search</button>
                {this.state.result.length === 0 ? null: this.state.searchType === "contestant" ? 
                <Contestant data={this.state.result}/> : this.state.searchType === "category" ? 
                <Category data={this.state.result}/> : <Badsearch data={this.state.result}/>}
            </div>
        )
    }
}

export default Search