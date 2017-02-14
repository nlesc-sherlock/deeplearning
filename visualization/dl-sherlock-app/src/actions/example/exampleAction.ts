import { EXAMPLE_ACTION }    from '../authorized-actions';

export const exampleAction = (imageSrc: string) => {
    return {
        type: EXAMPLE_ACTION,
        payload: { imageSrc }
    };
};
