import { deepFreeze } from './object.utils';


describe('Object utils', () => {
  const testObject = {
    testInnerObj: { innerTest1: 'one', innerTest2: 'two' } as any,
    testArray: ['Test1', 'Test2'],
    testArrayWithObjects: [
      { innerArrayProp: 'inner array prop' },
      { innerArrayProp: 'inner array prop' }
    ],
    testString: 'test'
  }

  it('should deep freeze the object', () => {
    // Clone the object as to not freeze the 'orignal' data reused throughout tests
    const clonedObject = JSON.parse(JSON.stringify((testObject)));
    const frozenObject = deepFreeze(clonedObject);

    // Object references should be equal
    expect(frozenObject).toBe(clonedObject);
    expect(frozenObject.testArray).toBe(clonedObject.testArray);
    expect(frozenObject.testArrayWithObjects[0]).toBe(clonedObject.testArrayWithObjects[0]);
    expect(frozenObject.testInnerObj).toBe(clonedObject.testInnerObj);

    // Values should equal
    expect(frozenObject).toEqual(clonedObject);

    // Objects should be recursively frozen
    expect(Object.isFrozen(frozenObject)).toBe(true);
    expect(Object.isFrozen(frozenObject.testInnerObj)).toBe(true);
    expect(Object.isFrozen(frozenObject.testArray)).toBe(true);
    expect(Object.isFrozen(frozenObject.testArrayWithObjects[0])).toBe(true);

    // Object mutation should throw
    expect(() => { delete frozenObject.testInnerObj }).toThrow(
      new TypeError('Cannot delete property \'testInnerObj\' of [object Object]'));
    expect(() => { frozenObject.testInnerObj = {} }).toThrow(
      new TypeError('Cannot assign to read only property \'testInnerObj\' of ' +
        'object \'[object Object]\''));
    expect(() => { frozenObject.testInnerObj.innerTest1 = 'test' }).toThrow(
      new TypeError('Cannot assign to read only property \'innerTest1\' of ' +
        'object \'[object Object]\''));
    expect(() => { frozenObject.testArray.push('Test X') }).toThrow(
      new TypeError('Cannot add property 2, object is not extensible'));
    expect(() => { frozenObject.testArrayWithObjects[0].innerArrayProp = 'Test' }).toThrow(
      new TypeError('Cannot assign to read only property \'innerArrayProp\' of ' +
        'object \'[object Object]\''));
    expect(() => { frozenObject.testString = '' }).toThrow(
      new TypeError('Cannot assign to read only property \'testString\' of ' +
        'object \'[object Object]\''));
  });
});
