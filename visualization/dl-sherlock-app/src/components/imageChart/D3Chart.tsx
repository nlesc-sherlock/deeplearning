import * as React from 'react';
import { connect } from 'react-redux'; 
// import { AppRegistry, View, Image } from 'react-native';

import * as d3 from 'd3';
import Faux from 'react-faux-dom';

import './D3Chart.css';

export interface ID3ChartProps extends React.Props<any> {
    data: any;
    img: any;
}

export interface IExtraProps {
    id: any;
}

export class UnconnectedD3Chart extends React.Component<ID3ChartProps & IExtraProps, {}> {
    private node: any;
    private imgHeight: number;
    private imgWidth: number;

    constructor() {
        super();
        this.imgHeight = 500,
        this.imgWidth  = 1000
    } 

    static mapStateToProps(state: any, myProps: IExtraProps) {    
        return {
            id: myProps.id,
            data: state.imageChart.d3JSON.images[myProps.id].objects,
            img: new Image(0,0)
        };
    }

    static mapDispatchToProps() {
        return {};
    }

    render(): JSX.Element {
        const props = this.props;
        let jsx = <div />;        
        
        // const jsxImage: JSX.Element = <img className='imgThumb' src={newImg.src} alt={props.id} />
        // jsx = jsxImage + node;
        
        let children: JSX.Element[] = [];
        
        const margin = { top: 0, right: 0, bottom: 0, left: 0 };
        let width = 300 - margin.left - margin.right;
        let height = 200 - margin.top - margin.bottom;

        const x = d3.scaleLinear().range([0, width]);
        const y = d3.scaleLinear().range([height, 0]);

        if (this.imgWidth && this.imgHeight) {
            width = this.imgWidth;
            height = this.imgHeight;

            x.domain([0, this.imgWidth]);
            y.domain([this.imgHeight, 0]);
        }            

        let node = Faux.createElement('svg');
        const svg = d3.select(node);
        svg.append("image")
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
            .attr('xlink:href', this.props.img.src)
            .attr('width', width)
            .attr('height', height);

        Object.keys(props.data).forEach((key: any) => {
            const data = props.data[key].bbox;
            
            svg.append('g')
                .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')')
                .attr('key', 'svg_'+key)
                .attr('class', 'rectClass')
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom);   
                
            if (data) {
                svg.append('rect')
                    .datum(data)
                    .attr('class', 'bar')
                    .attr('x', (d) => {
                        return x(d[0])
                    })
                    .attr('y', (d) => {
                        return y(d[1])
                    })
                    .attr('width', (d) => {
                        return x(d[2])
                    })
                    .attr('height', (d) => {
                        return y(d[3])
                    });
            }
            jsx = node.toReact();
            children.push(jsx);
        });
        
        // const jsxImage: JSX.Element = <img className='imgThumb' src={ this.props.img.src } alt={ props.id } />
        
        return (
            <span>
                {/*{jsxImage}*/}
                {children}
            </span>
        );
    }

    componentWillMount() {
        this.props.img.src = require('../../../images/' + this.props.id);
    }
}

export const D3Chart = connect(UnconnectedD3Chart.mapStateToProps,
    UnconnectedD3Chart.mapDispatchToProps)(UnconnectedD3Chart);
