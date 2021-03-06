import { Selector } from "testcafe";
import { RequestLogger } from 'testcafe';

const TEST_URL = process.env.TEST_URL;

const randomstring = require('randomstring');

const username = randomstring.generate();
const email = `${username}@test.com`
const password = "greaterthanten";

fixture("/register")
  .page(`${TEST_URL}/register`);

test(`should display the register form`, async (t) => {
  await t.navigateTo(`${TEST_URL}/register`)
    .expect(Selector("H1").withText("Register").exists).ok()
    .expect(Selector('form').exists).ok()
    .expect(Selector('input[disabled]').exists).ok()
    .expect(Selector('.validation-list').exists).ok()
    .expect(Selector('.validation-list > .error').nth(0).withText(
      'Username must not be greater than 5 characters.').exists).ok()
});

test(`should allow a user to register`, async (t) => {
  await t.navigateTo(`${TEST_URL}/register`)
    .typeText('input[name="username"]', username)
    .typeText('input[name="email"]', email)
    .typeText('input[name="password"]', password)
    .click(Selector('input[type="submit"]'));

  // assert user is redirected to '/'
  // assert '/' is displayed properly
  const tableRow = Selector('td').withText(username).parent();
  await t.expect(Selector('H1').withText('All Users').exists).ok()
    .expect(tableRow.child().withText(username).exists).ok()
    .expect(tableRow.child().withText(email).exists).ok();
});

test('should validate the password field', async t => {
  await t.navigateTo(`${TEST_URL}/register`)
    .expect(Selector('H1').withText('Register').exists).ok()
    .expect(Selector('form').exists).ok()
    .expect(Selector('input[disabled]').exists).ok()
    .expect(Selector('.validation-list > .error').nth(3).withText(
      'Password must be greater than 10 characters.').exists).ok()
    .typeText('input[name="password"]', 'greaterthanten')
    .expect(Selector('.validation-list').exists).ok()
    .expect(Selector('.validation-list > .error').nth(3).withText(
      'Password must be greater than 10 characters.').exists).notOk()
    .expect(Selector('.validation-list > .success').nth(0).withText(
      'Password must be greater than 10 characters.').exists).ok()
});

// test('should throw an error if the credentials are incorrect', async (t) => {
//   // will implement later
// });
