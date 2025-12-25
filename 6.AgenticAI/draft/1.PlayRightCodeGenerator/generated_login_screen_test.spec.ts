import { test, expect } from '@playwright/test';

test.describe('Login Functionality Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5173');
  });

  test('Successful Login', async ({ page }) => {
    await page.fill('input[name="company"]', 'ayurveda');
    await page.fill('input[name="email"]', 'example@domain.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button:has-text("Log In")');
    await expect(page.locator('text=Welcome')).toBeVisible(); // Adjust according to successful login message
  });

  test('Form Validation - Empty Fields', async ({ page }) => {
    await page.click('button:has-text("Log In")');
    await expect(page.locator('text=Please fill out this field')).toBeVisible();
  });

  test('Form Validation - Invalid Credentials', async ({ page }) => {
    await page.fill('input[name="company"]', 'wrongCompany');
    await page.fill('input[name="email"]', 'wrong@domain.com');
    await page.fill('input[name="password"]', 'wrongPassword');
    await page.click('button:has-text("Log In")');
    await expect(page.locator('text=Invalid username or password')).toBeVisible(); // Adjust according to error message
  });

  test('Verify Navigation After Successful Login', async ({ page }) => {
    await page.fill('input[name="company"]', 'ayurveda');
    await page.fill('input[name="email"]', 'example@domain.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button:has-text("Log In")');
    await expect(page).toHaveURL('http://localhost:5173/dashboard'); // Adjust expected URL after login
  });

});