import React,{Component} from "react"

class Appearances extends Component{
    constructor(props){
        super(props)
    }
    render(){
        return(
            <div>
                {"Appearances"} <br />
                {this.props.firstAppearance + " - " + this.props.lastAppearance}
            </div>
        )
    }
}

export default Appearances