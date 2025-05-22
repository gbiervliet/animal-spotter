const axios = require('axios');
const cheerio = require('cheerio');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const BASE_URL = "https://waarneming.nl/fieldwork/observations/explore/";

// Parse command line arguments
const argv = yargs(hideBin(process.argv))
  .option('end_date', {
    describe: 'End date for observations (YYYY-MM-DD)',
    default: '2025-05-21'
  })
  .option('point_coords', {
    describe: 'Point coordinates (format: lon%2Clat)',
    default: '5.854682922363281%2051.842903707882684'
  })
  .option('distance', {
    describe: 'Search radius distance in km',
    default: '5'
  })
  .option('species_id', {
    describe: 'Species ID to search for',
    default: '54'
  })
  .help()
  .argv;

async function fetchObservationData(url) {
  console.log('[*] Fetching JSON data...');
  try {
    const response = await axios.get(url);
    const data = response.data;

    if (!data.table) {
      throw new Error("Expected 'table' field in response JSON.");
    }

    return data.table;
  } catch (error) {
    console.error(`Error fetching data: ${error.message}`);
    process.exit(1);
  }
}

function htmlTableToJson(htmlTable) {
  console.log('[*] Parsing HTML table...');
  const $ = cheerio.load(htmlTable);
  const table = $('table');
  
  if (table.length === 0) {
    throw new Error("No <table> found.");
  }

  // Extract headers
  const headers = [];
  $('thead th', table).each(function() {
    headers.push($(this).text().trim());
  });

  // Extract rows
  const rows = [];
  $('tbody tr', table).each(function() {
    const rowData = {};
    $(this).find('td, th').each(function(i) {
      const key = i < headers.length ? headers[i] : `column_${i}`;
      if (key !== "" && key !== "Route") {
        rowData[key] = $(this).text().trim();
      }
    });
    rows.push(rowData);
  });

  return rows;
}

async function main() {
  const url = `${BASE_URL}?end_date=${argv.end_date}&json=species_observations&point=POINT(${argv.point_coords})&distance=${argv.distance}&species_id=${argv.species_id}`;
  
  try {
    const htmlTable = await fetchObservationData(url);
    const jsonData = htmlTableToJson(htmlTable);
    console.log(JSON.stringify(jsonData, null, 2));
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main(); 