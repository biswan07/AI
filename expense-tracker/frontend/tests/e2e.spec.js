
const { test, expect } = require('@playwright/test');
const path = require('path');

test.describe('Expense Tracker E2E', () => {

    test.beforeEach(async ({ request }) => {
        // Ensure clean state before each test
        await request.delete('http://127.0.0.1:5000/api/expenses/clear');
    });

    test('should load homepage and show empty state', async ({ page }) => {
        await page.goto('/');

        // Check title
        await expect(page).toHaveTitle(/Expense Tracker/);

        // Check header
        await expect(page.locator('h1')).toContainText('Expense Tracker');

        // Check for empty dashboard state
        await expect(page.locator('.dashboard-empty')).toBeVisible();
        await expect(page.locator('.dashboard-empty h2')).toContainText('No Data Yet');
    });

    test('should upload csv file and display dashboard', async ({ page }) => {
        await page.goto('/');

        // Upload file
        const fileInput = page.locator('input[type="file"]');
        await fileInput.setInputFiles(path.join(__dirname, 'fixtures/test_expenses.csv'));

        // Verify success message
        const message = page.locator('.message.success');
        await expect(message).toBeVisible();
        await expect(message).toContainText('Success! Processed 5 expenses');

        // Wait for dashboard to load (it waits for refresh)
        await expect(page.locator('.dashboard')).toBeVisible();

        // Check dashboard elements
        await expect(page.locator('.dashboard-header h1')).toContainText('SUMMARY');

        // Check charts exist
        await expect(page.locator('.charts-grid')).toBeVisible();

        // Verify some specific data points from the CSV
        // Total expenses should be 5
        await expect(page.locator('.dashboard-footer')).toContainText('Total Expenses Tracked: 5');

        // Check for top categories (Amazon = Servers/Computing, Uber = Transport, Starbucks = Dining, Netflix = Entertainment)
        const categoryList = page.locator('.category-list');
        await expect(categoryList).toBeVisible();
    });

    test('should clear data correctly', async ({ page, request }) => {
        // 1. Upload data first
        await page.goto('/');
        const fileInput = page.locator('input[type="file"]');
        await fileInput.setInputFiles(path.join(__dirname, 'fixtures/test_expenses.csv'));
        await expect(page.locator('.dashboard')).toBeVisible();

        // 2. Clear data via API
        await request.delete('http://127.0.0.1:5000/api/expenses/clear');

        // 3. Reload page and check for empty state
        await page.reload();
        await expect(page.locator('.dashboard-empty')).toBeVisible();
    });

});
