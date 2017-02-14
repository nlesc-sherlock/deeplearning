import * as React                   from 'react';
import { connect }                  from 'react-redux';

import './ExampleComponent.css';

export interface IExampleComponent {
    imageSrc : string;
}

export class UnconnectedExampleComponent extends React.Component<IExampleComponent, { }> {
    constructor() {
        super();
    }

    static mapStateToProps(state: any) {
        return {
            imageSrc: state.imageSrc
        };
    }

    static mapDispatchToProps() {
        return {};
    }

    render() {
        return (
            <div className="exampleDivClass">
                 <img src={ this.props.imageSrc } className="exampleImageClass" alt={ this.props.imageSrc }/>
            </div>
        );
    }
}

// Export just the connected component
export const ExampleComponent = connect(UnconnectedExampleComponent.mapStateToProps,
                                        UnconnectedExampleComponent.mapDispatchToProps)(UnconnectedExampleComponent);
