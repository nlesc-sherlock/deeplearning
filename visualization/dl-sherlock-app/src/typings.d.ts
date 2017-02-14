/* import all svg files as strings */
declare module '*.svg' {
    const __path__: string;
    export default __path__;
}

declare module 'classnames' {
    export default function classNames(classes:any): string;
}
