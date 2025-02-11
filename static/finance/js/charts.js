document.addEventListener('DOMContentLoaded', function () {

    // year data
    let chartYearLabels = [];

    // sale chart
    const saleChartElement = document.getElementById('SaleChart');
    const chartYearString = saleChartElement.getAttribute('data-year');
    const netSaleString = saleChartElement.getAttribute('data-net-sale');
    let netSaleData = [];

    // inventory chart
    const inventoryChartElement = document.getElementById('InventoryChart');
    const inventoryString = inventoryChartElement.getAttribute('data-inventory');
    let inventoryData = [];
    console.log(inventoryString)

    // asset chart
    const assetChartElement = document.getElementById("AssetChart");
    const currentAssetString = assetChartElement.getAttribute('data-current-asset');
    const nonCurrentAssetString = assetChartElement.getAttribute('data-non-current-asset');
    const totalAssetString = assetChartElement.getAttribute('data-total-asset');
    let currentAssetData = [];
    let nonCurrentAssetData = [];
    let totalAssetData = [];

    //debt chart
    const debtChartElement = document.getElementById("DebtChart");
    const currentDebtString = debtChartElement.getAttribute('data-current-debt');
    const nonCurrentDebtString = debtChartElement.getAttribute('data-non-current-debt');
    const totalDebtString = debtChartElement.getAttribute('data-total-debt');
    let currentDebtData = [];
    let nonCurrentDebtData = [];
    let totalDebtData = [];


    // //life cycle chart
    // const lifeCycleChartElement = document.getElementById("KdeChart");
    // const levelsString = lifeCycleChartElement.getAttribute('data-label-levels');
    // const heightString = lifeCycleChartElement.getAttribute('data-label-height');
    // const highLightString = lifeCycleChartElement.getAttribute('data-highlight-index');
    // let levelsData = [];
    // let heightData = [];
    // let highLightData = [];


    //Altman Bankrupsy chart
    const bankrupsyChartElement = document.getElementById("BankrupsyChart");
    const altmanBankrupsyString = bankrupsyChartElement.getAttribute('data-altman-bankrupsy');
    let altmanBankrupsyData = [];



    //Salary
    const salaryChartElement = document.getElementById("SalaryChart");
    const salaryFeeString = salaryChartElement.getAttribute('data-salary-fee');
    const productionFeeString = salaryChartElement.getAttribute('data-production-fee');
    const salaryProductionFeeString = salaryChartElement.getAttribute('data-salary-production-fee');

    let salaryFeeData = [];
    let productionFeeData = [];
    let salaryProductionFeeData = [];

    //Leverage Ratio
    const leverageChartElement = document.getElementById("LeverageChart");
    const debtRatioString = leverageChartElement.getAttribute('data-debt-ratio');
    const capitalRatioString = leverageChartElement.getAttribute('data-capital-ratio');
    const propertyRatioString = leverageChartElement.getAttribute('data-property-ratio');
    const equityPerTotalDebtString = leverageChartElement.getAttribute('data-equity-per-debt-ratio');
    const equityPerTotalNonCurrentAssetString = leverageChartElement.getAttribute('data-equity-per-asset-ratio');

    let debtRatioData = [];
    let capitalRatioData = [];
    let propertyRatioData = [];
    let equityPerTotalDebtRatio = [];
    let equityPerTotalNonCurrentAssetRatio = [];


    // Equity Chart
    const equityChartElement = document.getElementById("EquityChart");
    const totalEquityString = equityChartElement.getAttribute('total-equity');
    const totalSumEquityDebtString = equityChartElement.getAttribute('total-sum-equity-debt');

    let totalEquityData = [];
    let totalSumEquityDebtData = [];


    // Profitibility Chart
    const profitibilityChartElement = document.getElementById("ProfitibilityChart");

    const roaString = profitibilityChartElement.getAttribute('data-roa');
    const roabString = profitibilityChartElement.getAttribute('data-roab');
    const roeString = profitibilityChartElement.getAttribute('data-roe');
    const efficiencyString = profitibilityChartElement.getAttribute('data-efficiency');
    const grossProfitMarginString = profitibilityChartElement.getAttribute('data-gross-profit-margin');
    const netProfitMarginString = profitibilityChartElement.getAttribute('data-net-profit-margin');

    let roaData = [];
    let roabData = [];
    let roeData = [];
    let efficiencyData = [];
    let grossProfitMarginData = [];
    let netProfitMarginData = [];


    // Liquidity Chart
    const liquidityChartElement = document.getElementById('LiquidityChart');
    const instantRatioString = liquidityChartElement.getAttribute('data-instant-ratio');
    const currentRatioString = liquidityChartElement.getAttribute('data-current-ratio');

    let instantRatioData = [];
    let currentRatioData = [];

    // Agility Chart
    const agilityChartElement = document.getElementById('AgilityChart');
    const stockTurnOverString = agilityChartElement.getAttribute('data-stock-turnover');

    let stockTurnOverData = [];

    // Price Chart

    const priceChartElement = document.getElementById('PriceChart');
    const costructionOverheadString = priceChartElement.getAttribute('data-construction-overhead')
    const consumingMaterialString = priceChartElement.getAttribute('data-consuming-material')
    const productionTotalPriceString = priceChartElement.getAttribute('data-production-total-price')

    let costructionOverheadData = []
    let consumingMaterialData = []
    let productionTotalPriceData = []


    // Profit Chart

    const profitChartElement = document.getElementById('ProfitChart')
    const grossProfitString = profitChartElement.getAttribute('data-gross-profit')
    const operationProfitString = profitChartElement.getAttribute('data-operation-profit')
    const proceedProfitString = profitChartElement.getAttribute('data-proceed-profit')
    const netProfitString = profitChartElement.getAttribute('data-net-profit')

    let grossProfitData = [];
    let operationProfitData = [];
    let proceedProfitData = [];
    let netProfitData = [];

    try {
        // Year
        chartYearLabels = chartYearString ? JSON.parse(chartYearString) : [];

        // Sale
        netSaleData = netSaleString ? JSON.parse(netSaleString) : [];

        // Inventory
        inventoryData = inventoryString ? JSON.parse(inventoryString) : [];

        // Asset
        currentAssetData = currentAssetString ? JSON.parse(currentAssetString) : [];
        nonCurrentAssetData = nonCurrentAssetString ? JSON.parse(nonCurrentAssetString) : [];
        totalAssetData = totalAssetString ? JSON.parse(totalAssetString) : [];

        // Debt
        currentDebtData = currentDebtString ? JSON.parse(currentDebtString) : [];
        nonCurrentDebtData = nonCurrentDebtString ? JSON.parse(nonCurrentDebtString) : [];
        totalDebtData = totalDebtString ? JSON.parse(totalDebtString) : [];

        // // Life Cycle
        // levelsData = levelsString ? JSON.parse(levelsString.replace(/'/g, '"')) : [];
        // heightData = heightString ? JSON.parse(heightString) : [];
        // highLightData = highLightString ? JSON.parse(highLightString) : [];

        //Bankrupsy 
        altmanBankrupsyData = altmanBankrupsyString ? JSON.parse(altmanBankrupsyString) : [];

        // Salary 
        salaryFeeData = salaryFeeString ? JSON.parse(salaryFeeString) : [];
        productionFeeData = productionFeeString ? JSON.parse(productionFeeString) : [];
        salaryProductionFeeData = salaryProductionFeeString ? JSON.parse(salaryProductionFeeString) : [];

        // Leverage ratios
        debtRatioData = debtRatioString ? JSON.parse(debtRatioString) : [];
        capitalRatioData = capitalRatioString ? JSON.parse(capitalRatioString) : [];
        propertyRatioData = propertyRatioString ? JSON.parse(propertyRatioString) : [];
        equityPerTotalDebtRatio = equityPerTotalDebtString ? JSON.parse(equityPerTotalDebtString) : [];
        equityPerTotalNonCurrentAssetRatio = equityPerTotalNonCurrentAssetString ? JSON.parse(equityPerTotalNonCurrentAssetString) : [];


        // Equity 
        totalEquityData = totalEquityString ? JSON.parse(totalEquityString) : [];
        totalSumEquityDebtData = totalSumEquityDebtString ? JSON.parse(totalSumEquityDebtString) : [];



        // Liquidity
        instantRatioData = instantRatioString ? JSON.parse(instantRatioString) : [];
        currentRatioData = currentRatioString ? JSON.parse(currentRatioString) : [];

        // Agility 
        stockTurnOverData = stockTurnOverString ? JSON.parse(stockTurnOverString) : [];


        // Price
        costructionOverheadData = costructionOverheadString ? JSON.parse(costructionOverheadString) : [];
        consumingMaterialData = consumingMaterialString ? JSON.parse(consumingMaterialString) : [];
        productionTotalPriceData = productionTotalPriceString ? JSON.parse(productionTotalPriceString) : [];


        // Profit

        grossProfitData = grossProfitString ? JSON.parse(grossProfitString) : [];
        operationProfitData = operationProfitString ? JSON.parse(operationProfitString) : [];
        proceedProfitData = proceedProfitString ? JSON.parse(proceedProfitString) : [];
        netProfitData = netProfitString ? JSON.parse(netProfitString) : [];

        // Profitibility
        roaData = roaString ? JSON.parse(roaString) : [];
        roabData = roabString ? JSON.parse(roabString) : [];
        roeData = roeString ? JSON.parse(roeString) : [];
        efficiencyData = efficiencyString ? JSON.parse(efficiencyString) : [];
        grossProfitMarginData = grossProfitMarginString ? JSON.parse(grossProfitMarginString) : [];
        netProfitMarginData = netProfitMarginString ? JSON.parse(netProfitMarginString) : [];

        
    } catch (error) {
        console.error('Error parsing JSON data:', error);
    }

    console.log(grossProfitData)


    const length = chartYearLabels.length
    let lowRiskData = new Array(length)
    lowRiskData.fill(4)

    let midRiskData = new Array(length)
    midRiskData.fill(3)

    let highRiskData = new Array(length)
    highRiskData.fill(1.8)

    // Sale Chart
    const sale_chart_container = saleChartElement.getContext('2d');
    const saleChart = new Chart(sale_chart_container, {
        type: 'bar',
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'فروش خالص',
                    data: netSaleData,  // Use parsed array for data
                    borderColor: 'rgba(255, 99, 132, 1)',
                    backgroundColor: 'rgba(255, 99, 132, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار فروش'  // Title for the sale chart
                }
            },
            scales: {
                x: {
                    stacked: true, // Enable stacking on the X-axis
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const asset_chart_container = assetChartElement.getContext('2d');
    const assetChart = new Chart(asset_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'دارایی‌های جاری ',
                    data: currentAssetData,
                    borderColor: 'rgb(71, 203, 226)',
                    backgroundColor: 'rgba(71, 203, 226, .7)',
                    fill: true,  // Enable fill to stack the areas
                },

                {
                    label: 'دارایی‌های غیر جاری ',
                    data: nonCurrentAssetData,
                    borderColor: 'rgb(3, 120, 184)',
                    backgroundColor: 'rgb(3, 120, 184,.7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'مجموع دارایی‌های جاری و غیر جاری ',
                    data: totalAssetData,
                    borderColor: 'rgba(5, 160, 146,1)',
                    backgroundColor: ' rgba(5, 160, 146,.7)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار دارایی‌ها'  // Title for the debt chart
                }
            },
            scales: {

                x: {
                    stacked: true, // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }

            }
        }
    });

    const debt_chart_container = debtChartElement.getContext('2d');
    const debtChart = new Chart(debt_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'بدهی‌های جاری',
                    data: currentDebtData,
                    borderColor: '#F38584',
                    backgroundColor: 'rgb(243, 133, 132,.7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'بدهی‌های غیر جاری',
                    data: nonCurrentDebtData,
                    borderColor: '#85A49C',
                    backgroundColor: 'rgb(133, 164, 156, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'مجموع بدهی‌های جاری و غیر جاری',
                    data: totalDebtData,
                    borderColor: '#F6BE61',
                    backgroundColor: 'rgb(246, 190, 97, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار بدهی‌ها'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // const life_cycle_chart_container = lifeCycleChartElement.getContext('2d');

    // // Your x_vals and y_vals data (passed through Django template safely)
    // const x_vals = levelsData;
    // const y_vals = heightData;

    // // Let's say you want to highlight the 3rd point (index 2) dynamically
    // const highlightIndex = highLightData;

    // // Default color and size for all points
    // const pointColors = y_vals.map(() => 'rgb(12, 132, 135)');  // Default color for points
    // const pointSizes = y_vals.map(() => 5);  // Default size for points

    // // Change color and size for the specific point at 'highlightIndex'
    // pointColors[highlightIndex] = 'rgb(255, 99, 132)';  // Red color for the highlighted point
    // pointSizes[highlightIndex] = 10;  // Larger size for the highlighted point

    // // Create the chart
    // const kdeChart = new Chart(life_cycle_chart_container, {
    //     type: 'line',  // Specify chart type
    //     data: {
    //         labels: x_vals,
    //         datasets: [
    //             {
    //                 label: 'چرخه عمر',
    //                 data: y_vals,
    //                 borderColor: 'rgb(12, 132, 135)',
    //                 backgroundColor: 'rgba(12, 132, 135, .7)',
    //                 fill: true,  // Enable fill to stack the areas
    //                 pointBackgroundColor: pointColors,  // Set the dynamic point colors
    //                 pointRadius: pointSizes,  // Set the dynamic point sizes

    //                 tension: 0.1
    //             }
    //         ]
    //     },
    //     options: {
    //         plugins: {
    //             title: {
    //                 display: true,
    //                 text: 'نمودار چرخه عمر'  // Title for the chart
    //             }
    //         },
    //         scales: {
    //             x: {
    //                 stacked: true  // Enable stacking on the X-axis (optional for line)
    //             },
    //             y: {
    //                 beginAtZero: true
    //             }
    //         }
    //     }
    // });
    const inventory_chart_container = inventoryChartElement.getContext('2d');
    const inventoryChart = new Chart(inventory_chart_container, {
        type: 'bar',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'موجودی انبار',
                    data: inventoryData,
                    borderColor: 'rgb(230, 58, 70)',
                    backgroundColor: 'rgb(230, 58, 70, .7)',
                    fill: true,  // Enable fill to stack the areas
                }
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'انبار'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    const bankrupsy_chart_container = bankrupsyChartElement.getContext('2d');
    const bankrupsyChart = new Chart(bankrupsy_chart_container, {
        type: 'bar',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [

                {
                    label: 'جایگاه در سال جاری',
                    data: altmanBankrupsyData,
                    type: 'line', // Set this dataset type to 'line'
                    fill: false,
                    borderColor: 'rgb(28, 29, 104)', // Line color
                    backgroundColor: 'rgb(28, 29, 104)', // Point color
                    borderWidth: 2
                },
                {
                    label: 'احتمال ورشکستی بالا',
                    data: highRiskData,
                    backgroundColor: 'rgb(252, 48, 61,1)', // Bar color
                    borderColor: 'rgb(252, 48, 61)',
                    borderWidth: 1
                },

                {
                    label: 'احتمال ورشکستی متوسط',
                    data: midRiskData,
                    backgroundColor: 'rgb(237, 202, 62,1)', // Bar color
                    borderColor: 'rgb(237, 202, 62)',
                    borderWidth: 1
                },
                {
                    label: 'احتمال ورشکستگی پایین',
                    data: lowRiskData,
                    backgroundColor: 'rgb(5, 160, 146,1)', // Bar color
                    borderColor: 'rgb(5, 160, 146))',
                    borderWidth: 1
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار احتمال ورشکستگی'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const leveragechart_container = document.getElementById('LeverageChart').getContext('2d');
    const leverageChart = new Chart(leveragechart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'نسبت بدهی',
                    data: debtRatioData,
                    borderColor: 'rgb(230, 111, 79)',
                    backgroundColor: 'rgb(230, 111, 79, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'نسبت سرمایه',
                    data: capitalRatioData,
                    borderColor: 'rgb(233, 196, 107)',
                    backgroundColor: 'rgb(233, 196, 107, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'نسبت مالکانه',
                    data: propertyRatioData,
                    borderColor: 'rgb(242, 163, 96)',
                    backgroundColor: 'rgb(242, 163, 96, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'نسبت حقوق صاحبان سهام به کل بدهی‌ها',
                    data: equityPerTotalDebtRatio,
                    borderColor: 'rgb(42, 157, 142)',
                    backgroundColor: 'rgb(42, 157, 142, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'نسبت حقوق صاحبان سهام به کل دارایی‌های ثابت',
                    data: equityPerTotalNonCurrentAssetRatio,
                    borderColor: 'rgb(40, 69, 83)',
                    backgroundColor: 'rgb(40, 69, 83, .7)',
                    fill: true,  // Enable fill to stack the areas
                },


            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نسبت‌های اهرمی'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                }
            }
        }
    });
    const salary_chart_container = salaryChartElement.getContext('2d');
    const salarychart = new Chart(salary_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'دستمزد غیرمتسقیم',
                    data: salaryFeeData,
                    borderColor: 'rgb(69, 123, 157)',
                    backgroundColor: 'rgb(69, 123, 157 , .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'دستمزد مستقیم',
                    data: productionFeeData,
                    borderColor: 'rgb(168, 217, 221)',
                    backgroundColor: 'rgb(168, 217, 221, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: ' جمع دستمزد مستقیم و دستمزد غیر مستقیم',
                    data: salaryProductionFeeData,
                    borderColor: 'rgb(230, 58, 70)',
                    backgroundColor: 'rgb(230, 58, 70, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'دستمزد'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const equity_chart_container = document.getElementById('EquityChart').getContext('2d');
    const equityChart = new Chart(equity_chart_container, {
        type: ['line'],  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'جمع حقوق صاحبان سهام',
                    data: totalEquityData,
                    borderColor: 'rgb(97, 107, 57)',
                    backgroundColor: 'rgb(97, 107, 57, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'جمع بدهی‌های جاری و غیرجاری',
                    data: totalDebtData,
                    borderColor: 'rgb(253, 250, 223)',
                    backgroundColor: 'rgb(253, 250, 223, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'جمع بدهی‌ها و حقوق صاحبان سهام',
                    data: totalSumEquityDebtData,
                    borderColor: 'rgb(187, 110, 38)',
                    backgroundColor: 'rgb(187, 110, 38, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار حقوق صاحبان سهام'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const profitibilitychart_container = profitibilityChartElement.getContext('2d');
    const profitibilityChart = new Chart(profitibilitychart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [

                {
                    label: 'ROA',
                    data: roaData,
                    borderColor: 'rgb(75, 201, 241)',
                    backgroundColor: 'rgb(75, 201, 241, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'ROA`',
                    data: roabData,
                    borderColor: 'rgb(63, 55, 202)',
                    backgroundColor: 'rgb(63, 55, 202, .7)',
                    fill: true,  // Enable fill to stack the areas
                },

                {
                    label: 'اثربخشی',
                    data: efficiencyData,
                    borderColor: 'rgb(21, 226, 220)',
                    backgroundColor: 'rgb(21, 226, 220, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'حاشیه سود ناخالص',
                    data: grossProfitMarginData,
                    borderColor: 'rgb(180, 24, 159)',
                    backgroundColor: 'rgb(180, 24, 159, 0.7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'حاشیه سود خالص',
                    data: netProfitMarginData,
                    borderColor: 'rgb(249, 37, 133)',
                    backgroundColor: 'rgb(249, 37, 133, 0.7)',
                    fill: true,
                },
                {
                    label: 'ROE',
                    data: roeData,
                    borderColor: 'rgba(0, 0, 0, 1)',
                    backgroundColor: 'rgba(0, 0, 0, .5)',
                    fill: true,  // Enable fill to stack the areas
                },


            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نسبت‌های سود‌اوری'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                }
            }
        }
    });

    const liquidity_chart_container = liquidityChartElement.getContext('2d');
    const liquiditychart = new Chart(liquidity_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'نسبت آنی',
                    data: instantRatioData,
                    borderColor: 'rgb(72, 203, 223)',
                    backgroundColor: 'rgb(72, 203, 223, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'نسبت جاری',
                    data: currentRatioData,
                    borderColor: 'rgb(1, 2, 95)',
                    backgroundColor: 'rgb(1, 2, 95, .7)',
                    fill: true,  // Enable fill to stack the areas
                },


            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نمودار نقدینگی'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const agility_chart_container = agilityChartElement.getContext('2d');
    const agilityChart = new Chart(agility_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'نسبت آنی',
                    data: instantRatioData,
                    borderColor: 'rgb(21, 32, 62)',
                    backgroundColor: 'rgb(21, 32, 62, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'گردش موجودی انبار',
                    data: stockTurnOverData,
                    borderColor: 'rgb(252, 163, 17)',
                    backgroundColor: 'rgb(252, 163, 17, .7)',
                    fill: true,  // Enable fill to stack the areas
                },

            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'نسبت‌های چابکی'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    // <!-- #Price Chart-- >
    const price_chart_container = priceChartElement.getContext('2d');
    const priceChart = new Chart(price_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'سربار ساخت',
                    data: costructionOverheadData,
                    borderColor: 'rgba(255, 35, 132, 1)',
                    backgroundColor: 'rgba(255, 35, 132, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'دستمزد مستقیم',
                    data: productionFeeData,
                    borderColor: 'rgba(255, 194, 132, 1)',
                    backgroundColor: 'rgba(255, 194, 132, .5)',
                    fill: true,  // Enable fill to stack the areas
                },

                {
                    label: 'مواد مستقیم مصرفی',
                    data: consumingMaterialData,
                    borderColor: 'rgb(107, 112, 90)',
                    backgroundColor: 'rgb(107, 112, 90, .7)',
                    fill: true,  // Enable fill to stack the areas
                },

                {
                    label: 'جمع هزینه‌های تولید',
                    data: productionTotalPriceData,
                    borderColor: 'rgb(182, 184, 162)',
                    backgroundColor: 'rgb(182, 184, 162, .7)',
                    fill: true,  // Enable fill to stack the areas
                },


            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'هزینه‌ها'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    const profit_chart_container = profitChartElement.getContext('2d');
    const profitChart = new Chart(profit_chart_container, {
        type: 'line',  // Specify chart type
        data: {
            labels: chartYearLabels,
            datasets: [
                {
                    label: 'سود ناخالص',
                    data: grossProfitData,
                    borderColor: 'rgb(252, 164, 6)',
                    backgroundColor: 'rgb(252, 164, 6, .7)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'سود عملیاتی',
                    data: operationProfitData,
                    borderColor: 'rgb(222, 46, 0)',
                    backgroundColor: 'rgb(222, 46, 0, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'سود ویژه',
                    data: proceedProfitData,
                    borderColor: 'rgb(105, 2, 14)',
                    backgroundColor: 'rgb(105, 2, 14, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'سود خالص',
                    data: netProfitData,
                    borderColor: 'rgb(0, 5, 29)',
                    backgroundColor: 'rgb(0, 5, 29, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
                {
                    label: 'فروش خالص',
                    data: netSaleData,
                    borderColor: 'rgba(25, 99, 132, 1)',
                    backgroundColor: 'rgba(25, 99, 132, .5)',
                    fill: true,  // Enable fill to stack the areas
                },
            ]
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'سود'  // Title for the debt chart
                }
            },
            scales: {
                x: {
                    stacked: true  // Enable stacking on the X-axis (optional for line)
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});