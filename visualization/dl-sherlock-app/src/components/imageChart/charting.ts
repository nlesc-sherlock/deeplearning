/// <reference path='../../../node_modules/@types/d3/index.d.ts'/>;
import * as d3 from 'd3';

export module charting {
    export class Chart {
        private _container: d3.Selection<SVGElement, {}, HTMLElement, any>;
        private _group: d3.Selection<SVGElement, {}, HTMLElement, any>;
        // private _paddingLeft = 50;
        // private _paddingBottom = 30;
        // private _paddingTop = 30;
        // private _width: number;
        // private _height: number;
        // private _ratio = 3 / 4;

        private margin = {top: 20, right: 20, bottom: 50, left: 70};
        private width = 960 - this.margin.left - this.margin.right;
        private height = 500 - this.margin.top - this.margin.bottom;

        private _xAxis: d3.Axis<any>;
        private _yAxis: d3.Axis<any>;

        // private _dataGroup: d3.Selection<SVGElement, {}, HTMLElement, any>;

        constructor(containerId: string) {
            this.init(containerId);
        }

        private init(containerId: string) {
            const selection = d3.select<SVGElement, {}>(containerId);
            this._container = selection;

            this._xAxis = d3.axisBottom(d3.scaleLinear().range([0, this.width]));
            this._yAxis = d3.axisLeft(d3.scaleLinear().range([this.height, 0]));

            // var valueline = d3.line()
            //     .x((d) => { return x(d.date); })
            //     .y((d) => { return y(d.close); });

            const svg = selection.append<SVGElement>('svg')
                .attr('width', this.width + this.margin.left + this.margin.right)
                .attr('height', this.height + this.margin.top + this.margin.bottom)
                .append('g')
                .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')');

            this._group = svg.append<SVGElement>('g')
                .attr('transform', 'translate(0,' + this.height + ')');

            // const node = selection.node();

            // // if (node !== null) {
            //     const width = node.clientWidth;
            //     const height = node.clientHeight;

            //     const svg = selection.append<SVGElement>('svg');
            //     this._group = svg.append<SVGElement>('g');

            //     const xscale = d3.scaleLinear().range([0, width]);
            //     const yscale = d3.scaleLinear().range([0, height]);
            //     this._xAxis = d3.axisBottom(xscale);

            //     // this._xAxis.translate(this._paddingLeft, (this._height - this._paddingBottom));
            //     // this._yAxis = new yAxis(this._group, 1);
            //     // this._yAxis.translate(this._paddingLeft, this._paddingTop);
            // // }
        }

        draw() {
            this._group.call(this._xAxis);
            this._group.call(this._yAxis);
        }
    }
}
