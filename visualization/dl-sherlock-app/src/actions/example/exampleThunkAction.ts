import { EXAMPLE_THUNK_ACTION }    from '../authorized-actions';

export const exampleThunkAction = (imageSrc: string) => {
    return {
        type: EXAMPLE_THUNK_ACTION,
        payload: { imageSrc }
    };
};
